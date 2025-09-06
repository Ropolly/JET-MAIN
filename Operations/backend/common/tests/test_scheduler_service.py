"""
Django test cases for scheduler service functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from unittest.mock import patch, Mock
import threading
import time
from datetime import datetime, timedelta
from django.utils import timezone
from common.services.scheduler_service import SchedulerService, get_scheduler, schedule_task, schedule_daily_task


class SchedulerServiceTestCase(TestCase):
    """Test case for scheduler service functionality."""
    
    def setUp(self):
        """Set up test data for scheduler service tests."""
        self.scheduler = SchedulerService()
        self.test_results = []
    
    def test_task_function(self, message="test"):
        """Simple test function for scheduler testing."""
        self.test_results.append(f"Task executed: {message}")
        return f"Task completed: {message}"
    
    def test_schedule_task_success(self):
        """Test successful task scheduling."""
        result = self.scheduler.schedule_task(
            "test_task",
            self.test_task_function,
            60,
            "test_message"
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertIn("test_task", self.scheduler.scheduled_tasks)
        
        task_info = self.scheduler.scheduled_tasks["test_task"]
        self.assertEqual(task_info['func'], self.test_task_function)
        self.assertEqual(task_info['interval'], 60)
        self.assertEqual(task_info['args'], ("test_message",))
        self.assertTrue(task_info['active'])
    
    def test_schedule_daily_task_success(self):
        """Test successful daily task scheduling."""
        result = self.scheduler.schedule_daily_task(
            "daily_test",
            self.test_task_function,
            9,
            30,
            "daily_message"
        )
        
        # Assertions
        self.assertTrue(result)
        self.assertIn("daily_test", self.scheduler.scheduled_tasks)
        
        task_info = self.scheduler.scheduled_tasks["daily_test"]
        self.assertEqual(task_info['interval'], 86400)  # 24 hours
        self.assertTrue(task_info.get('daily', False))
        self.assertEqual(task_info['hour'], 9)
        self.assertEqual(task_info['minute'], 30)
    
    def test_unschedule_task_success(self):
        """Test successful task unscheduling."""
        # First schedule a task
        self.scheduler.schedule_task("temp_task", self.test_task_function, 60)
        self.assertIn("temp_task", self.scheduler.scheduled_tasks)
        
        # Then unschedule it
        result = self.scheduler.unschedule_task("temp_task")
        
        # Assertions
        self.assertTrue(result)
        self.assertNotIn("temp_task", self.scheduler.scheduled_tasks)
    
    def test_unschedule_nonexistent_task(self):
        """Test unscheduling a non-existent task."""
        result = self.scheduler.unschedule_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_run_task_now_success(self):
        """Test running a scheduled task immediately."""
        # Schedule a task
        self.scheduler.schedule_task("immediate_task", self.test_task_function, 3600, "immediate")
        
        # Run it immediately
        result = self.scheduler.run_task_now("immediate_task")
        
        # Assertions
        self.assertTrue(result)
        
        # Wait a moment for the task to complete
        time.sleep(0.1)
        
        # Check if task was executed
        self.assertIn("Task executed: immediate", self.test_results)
    
    def test_run_nonexistent_task(self):
        """Test running a non-existent task."""
        result = self.scheduler.run_task_now("nonexistent_task")
        self.assertFalse(result)
    
    def test_get_task_status_success(self):
        """Test getting task status for existing task."""
        # Schedule a task
        self.scheduler.schedule_task("status_task", self.test_task_function, 120)
        
        # Get status
        status = self.scheduler.get_task_status("status_task")
        
        # Assertions
        self.assertIsNotNone(status)
        self.assertEqual(status['name'], "status_task")
        self.assertEqual(status['interval'], 120)
        self.assertTrue(status['active'])
        self.assertEqual(status['run_count'], 0)
        self.assertFalse(status['is_running'])
        self.assertIsNone(status['last_run'])
    
    def test_get_task_status_nonexistent(self):
        """Test getting status for non-existent task."""
        status = self.scheduler.get_task_status("nonexistent_task")
        self.assertIsNone(status)
    
    def test_list_scheduled_tasks(self):
        """Test listing all scheduled tasks."""
        # Schedule multiple tasks
        self.scheduler.schedule_task("task1", self.test_task_function, 60)
        self.scheduler.schedule_task("task2", self.test_task_function, 120)
        self.scheduler.schedule_daily_task("daily_task", self.test_task_function, 10, 0)
        
        # List tasks
        tasks = self.scheduler.list_scheduled_tasks()
        
        # Assertions
        self.assertEqual(len(tasks), 3)
        task_names = [task['name'] for task in tasks]
        self.assertIn("task1", task_names)
        self.assertIn("task2", task_names)
        self.assertIn("daily_task", task_names)
    
    def test_pause_and_resume_task(self):
        """Test pausing and resuming a task."""
        # Schedule a task
        self.scheduler.schedule_task("pause_test", self.test_task_function, 60)
        
        # Pause the task
        result = self.scheduler.pause_task("pause_test")
        self.assertTrue(result)
        
        # Check if task is paused
        status = self.scheduler.get_task_status("pause_test")
        self.assertFalse(status['active'])
        
        # Resume the task
        result = self.scheduler.resume_task("pause_test")
        self.assertTrue(result)
        
        # Check if task is active again
        status = self.scheduler.get_task_status("pause_test")
        self.assertTrue(status['active'])
    
    def test_pause_nonexistent_task(self):
        """Test pausing a non-existent task."""
        result = self.scheduler.pause_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_resume_nonexistent_task(self):
        """Test resuming a non-existent task."""
        result = self.scheduler.resume_task("nonexistent_task")
        self.assertFalse(result)
    
    def test_scheduler_start_stop(self):
        """Test starting and stopping the scheduler."""
        # Start scheduler
        self.scheduler.start_scheduler()
        
        # Check if scheduler thread is running
        self.assertTrue(hasattr(self.scheduler, '_scheduler_thread'))
        self.assertTrue(self.scheduler._scheduler_thread.is_alive())
        
        # Stop scheduler
        self.scheduler.stop_scheduler()
        
        # Wait for thread to stop
        time.sleep(0.1)
        
        # Check if stop event is set
        self.assertTrue(self.scheduler._stop_event.is_set())
    
    def test_task_execution_with_error(self):
        """Test task execution when task function raises an error."""
        def error_task():
            raise Exception("Test error")
        
        # Schedule error task
        self.scheduler.schedule_task("error_task", error_task, 60)
        
        # Run task (should not crash scheduler)
        result = self.scheduler.run_task_now("error_task")
        self.assertTrue(result)
        
        # Wait for task to complete
        time.sleep(0.1)
        
        # Task should still be in scheduled tasks
        self.assertIn("error_task", self.scheduler.scheduled_tasks)
    
    def test_task_update_existing(self):
        """Test updating an existing scheduled task."""
        # Schedule initial task
        self.scheduler.schedule_task("update_task", self.test_task_function, 60, "original")
        original_next_run = self.scheduler.scheduled_tasks["update_task"]['next_run']
        
        # Update the task
        self.scheduler.schedule_task("update_task", self.test_task_function, 120, "updated")
        
        # Assertions
        task_info = self.scheduler.scheduled_tasks["update_task"]
        self.assertEqual(task_info['interval'], 120)
        self.assertEqual(task_info['args'], ("updated",))
        # Next run time should be updated
        self.assertNotEqual(task_info['next_run'], original_next_run)
    
    def test_global_scheduler_instance(self):
        """Test global scheduler instance functionality."""
        scheduler1 = get_scheduler()
        scheduler2 = get_scheduler()
        
        # Should return the same instance
        self.assertIs(scheduler1, scheduler2)
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        # Test schedule_task convenience function
        result = schedule_task("conv_task", self.test_task_function, 60, "convenience")
        self.assertTrue(result)
        
        # Test schedule_daily_task convenience function
        result = schedule_daily_task("conv_daily", self.test_task_function, 12, 0, "daily_convenience")
        self.assertTrue(result)
        
        # Verify tasks were scheduled in global scheduler
        global_scheduler = get_scheduler()
        self.assertIn("conv_task", global_scheduler.scheduled_tasks)
        self.assertIn("conv_daily", global_scheduler.scheduled_tasks)
    
    def test_daily_task_next_run_calculation(self):
        """Test next run calculation for daily tasks."""
        now = timezone.now()
        current_hour = now.hour
        
        # Schedule daily task for an hour that has already passed today
        past_hour = (current_hour - 1) % 24
        self.scheduler.schedule_daily_task("past_daily", self.test_task_function, past_hour, 0)
        
        task_info = self.scheduler.scheduled_tasks["past_daily"]
        next_run = task_info['next_run']
        
        # Next run should be tomorrow
        self.assertGreater(next_run, now)
        self.assertEqual(next_run.hour, past_hour)
        
        # Schedule daily task for a future hour today
        future_hour = (current_hour + 1) % 24
        self.scheduler.schedule_daily_task("future_daily", self.test_task_function, future_hour, 0)
        
        task_info = self.scheduler.scheduled_tasks["future_daily"]
        next_run = task_info['next_run']
        
        # Next run should be today (if future hour is later today) or tomorrow
        self.assertGreater(next_run, now)
        self.assertEqual(next_run.hour, future_hour)
    
    def tearDown(self):
        """Clean up after tests."""
        # Stop scheduler if running
        if hasattr(self.scheduler, '_scheduler_thread') and self.scheduler._scheduler_thread.is_alive():
            self.scheduler.stop_scheduler()
        
        # Clear test results
        self.test_results.clear()


class CelerySchedulerServiceTestCase(TestCase):
    """Test case for Celery scheduler service functionality."""
    
    def setUp(self):
        """Set up test data for Celery scheduler tests."""
        # Skip if Celery is not available
        try:
            from common.services.scheduler_service import CelerySchedulerService
            self.celery_service = CelerySchedulerService()
        except ImportError:
            self.skipTest("Celery not available")
    
    def test_celery_service_initialization(self):
        """Test Celery scheduler service initialization."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        self.assertIsNotNone(service.app)
        self.assertEqual(service.app.main, 'jet_operations')
    
    def test_schedule_interval_task(self):
        """Test scheduling an interval-based task with Celery."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_interval",
            task_path="myapp.tasks.test_task",
            schedule_type="interval",
            seconds=300
        )
        
        self.assertTrue(result)
        self.assertIn("test_interval", service.app.conf.beat_schedule)
    
    def test_schedule_crontab_task(self):
        """Test scheduling a crontab-based task with Celery."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_crontab",
            task_path="myapp.tasks.daily_task",
            schedule_type="crontab",
            hour=9,
            minute=30
        )
        
        self.assertTrue(result)
        self.assertIn("test_crontab", service.app.conf.beat_schedule)
    
    def test_unsupported_schedule_type(self):
        """Test scheduling with unsupported schedule type."""
        from common.services.scheduler_service import CelerySchedulerService
        
        service = CelerySchedulerService()
        
        result = service.schedule_periodic_task(
            task_name="test_unsupported",
            task_path="myapp.tasks.test_task",
            schedule_type="unsupported"
        )
        
        self.assertFalse(result)
