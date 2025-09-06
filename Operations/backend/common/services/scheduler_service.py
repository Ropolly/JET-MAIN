"""
Scheduler Service for Common Operations

Moved from utils/schedulers/ to common/services/scheduler_service.py
This service handles scheduled tasks and background job management.
"""

import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from typing import Optional, Dict, Any, List, Callable
import threading
import time

logger = logging.getLogger(__name__)

try:
    from celery import Celery
    from celery.schedules import crontab
    CELERY_AVAILABLE = True
except ImportError:
    logger.warning("Celery not installed. Install with: pip install celery")
    Celery = None
    crontab = None
    CELERY_AVAILABLE = False


class SchedulerService:
    """
    Service for managing scheduled tasks and background jobs
    """
    
    def __init__(self):
        self.scheduled_tasks = {}
        self.running_tasks = {}
        self._stop_event = threading.Event()
        
    def schedule_task(self, task_name: str, func: Callable, interval_seconds: int, 
                     *args, **kwargs) -> bool:
        """
        Schedule a recurring task
        
        Args:
            task_name: Unique name for the task
            func: Function to execute
            interval_seconds: Interval between executions in seconds
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            bool: True if scheduled successfully
        """
        try:
            if task_name in self.scheduled_tasks:
                logger.warning(f"Task {task_name} already scheduled, updating...")
                self.unschedule_task(task_name)
            
            task_info = {
                'func': func,
                'interval': interval_seconds,
                'args': args,
                'kwargs': kwargs,
                'next_run': timezone.now() + timedelta(seconds=interval_seconds),
                'last_run': None,
                'run_count': 0,
                'active': True
            }
            
            self.scheduled_tasks[task_name] = task_info
            logger.info(f"Scheduled task '{task_name}' to run every {interval_seconds} seconds")
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling task {task_name}: {str(e)}")
            return False
    
    def schedule_daily_task(self, task_name: str, func: Callable, hour: int = 0, 
                           minute: int = 0, *args, **kwargs) -> bool:
        """
        Schedule a daily recurring task
        
        Args:
            task_name: Unique name for the task
            func: Function to execute
            hour: Hour to run (0-23)
            minute: Minute to run (0-59)
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            bool: True if scheduled successfully
        """
        try:
            # Calculate next run time
            now = timezone.now()
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time has already passed today, schedule for tomorrow
            if next_run <= now:
                next_run += timedelta(days=1)
            
            task_info = {
                'func': func,
                'interval': 86400,  # 24 hours in seconds
                'args': args,
                'kwargs': kwargs,
                'next_run': next_run,
                'last_run': None,
                'run_count': 0,
                'active': True,
                'daily': True,
                'hour': hour,
                'minute': minute
            }
            
            self.scheduled_tasks[task_name] = task_info
            logger.info(f"Scheduled daily task '{task_name}' to run at {hour:02d}:{minute:02d}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling daily task {task_name}: {str(e)}")
            return False
    
    def unschedule_task(self, task_name: str) -> bool:
        """
        Remove a scheduled task
        
        Args:
            task_name: Name of the task to remove
            
        Returns:
            bool: True if removed successfully
        """
        try:
            if task_name in self.scheduled_tasks:
                del self.scheduled_tasks[task_name]
                logger.info(f"Unscheduled task '{task_name}'")
                return True
            else:
                logger.warning(f"Task '{task_name}' not found in scheduled tasks")
                return False
                
        except Exception as e:
            logger.error(f"Error unscheduling task {task_name}: {str(e)}")
            return False
    
    def run_task_now(self, task_name: str) -> bool:
        """
        Execute a scheduled task immediately
        
        Args:
            task_name: Name of the task to run
            
        Returns:
            bool: True if executed successfully
        """
        try:
            if task_name not in self.scheduled_tasks:
                logger.error(f"Task '{task_name}' not found")
                return False
            
            task_info = self.scheduled_tasks[task_name]
            
            if task_name in self.running_tasks:
                logger.warning(f"Task '{task_name}' is already running")
                return False
            
            # Execute the task in a separate thread
            thread = threading.Thread(
                target=self._execute_task,
                args=(task_name, task_info),
                daemon=True
            )
            thread.start()
            
            return True
            
        except Exception as e:
            logger.error(f"Error running task {task_name}: {str(e)}")
            return False
    
    def _execute_task(self, task_name: str, task_info: Dict[str, Any]):
        """Execute a task and handle errors"""
        try:
            self.running_tasks[task_name] = {
                'start_time': timezone.now(),
                'thread': threading.current_thread()
            }
            
            logger.info(f"Executing task '{task_name}'")
            
            # Call the task function
            result = task_info['func'](*task_info['args'], **task_info['kwargs'])
            
            # Update task info
            task_info['last_run'] = timezone.now()
            task_info['run_count'] += 1
            
            # Calculate next run time
            if task_info.get('daily', False):
                # For daily tasks, schedule for next day at same time
                next_run = task_info['last_run'].replace(
                    hour=task_info['hour'],
                    minute=task_info['minute'],
                    second=0,
                    microsecond=0
                ) + timedelta(days=1)
            else:
                # For interval tasks, add interval to last run
                next_run = task_info['last_run'] + timedelta(seconds=task_info['interval'])
            
            task_info['next_run'] = next_run
            
            logger.info(f"Task '{task_name}' completed successfully. Next run: {next_run}")
            
        except Exception as e:
            logger.error(f"Error executing task '{task_name}': {str(e)}")
            
        finally:
            # Remove from running tasks
            if task_name in self.running_tasks:
                del self.running_tasks[task_name]
    
    def start_scheduler(self):
        """Start the task scheduler in a background thread"""
        if hasattr(self, '_scheduler_thread') and self._scheduler_thread.is_alive():
            logger.warning("Scheduler is already running")
            return
        
        self._stop_event.clear()
        self._scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self._scheduler_thread.start()
        logger.info("Task scheduler started")
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self._stop_event.set()
        if hasattr(self, '_scheduler_thread'):
            self._scheduler_thread.join(timeout=5)
        logger.info("Task scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop"""
        while not self._stop_event.is_set():
            try:
                now = timezone.now()
                
                # Check each scheduled task
                for task_name, task_info in list(self.scheduled_tasks.items()):
                    if not task_info.get('active', True):
                        continue
                    
                    if task_name in self.running_tasks:
                        continue  # Task is already running
                    
                    if now >= task_info['next_run']:
                        # Time to run this task
                        thread = threading.Thread(
                            target=self._execute_task,
                            args=(task_name, task_info),
                            daemon=True
                        )
                        thread.start()
                
                # Sleep for a short interval before checking again
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                time.sleep(30)  # Wait longer on error
    
    def get_task_status(self, task_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a scheduled task
        
        Args:
            task_name: Name of the task
            
        Returns:
            dict: Task status information or None if not found
        """
        if task_name not in self.scheduled_tasks:
            return None
        
        task_info = self.scheduled_tasks[task_name]
        is_running = task_name in self.running_tasks
        
        status = {
            'name': task_name,
            'active': task_info.get('active', True),
            'interval': task_info['interval'],
            'next_run': task_info['next_run'],
            'last_run': task_info['last_run'],
            'run_count': task_info['run_count'],
            'is_running': is_running
        }
        
        if is_running:
            running_info = self.running_tasks[task_name]
            status['running_since'] = running_info['start_time']
            status['running_duration'] = timezone.now() - running_info['start_time']
        
        return status
    
    def list_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """
        List all scheduled tasks with their status
        
        Returns:
            list: List of task status dictionaries
        """
        tasks = []
        for task_name in self.scheduled_tasks:
            status = self.get_task_status(task_name)
            if status:
                tasks.append(status)
        
        return tasks
    
    def pause_task(self, task_name: str) -> bool:
        """
        Pause a scheduled task (it won't run until resumed)
        
        Args:
            task_name: Name of the task to pause
            
        Returns:
            bool: True if paused successfully
        """
        if task_name not in self.scheduled_tasks:
            logger.error(f"Task '{task_name}' not found")
            return False
        
        self.scheduled_tasks[task_name]['active'] = False
        logger.info(f"Paused task '{task_name}'")
        return True
    
    def resume_task(self, task_name: str) -> bool:
        """
        Resume a paused task
        
        Args:
            task_name: Name of the task to resume
            
        Returns:
            bool: True if resumed successfully
        """
        if task_name not in self.scheduled_tasks:
            logger.error(f"Task '{task_name}' not found")
            return False
        
        self.scheduled_tasks[task_name]['active'] = True
        logger.info(f"Resumed task '{task_name}'")
        return True


class CelerySchedulerService:
    """
    Celery-based scheduler service for production environments
    """
    
    def __init__(self):
        if not CELERY_AVAILABLE:
            raise ImportError("Celery is required for CelerySchedulerService")
        
        self.app = Celery('jet_operations')
        self.app.config_from_object('django.conf:settings', namespace='CELERY')
        self.app.autodiscover_tasks()
    
    def schedule_periodic_task(self, task_name: str, task_path: str, 
                              schedule_type: str = 'interval', **schedule_kwargs):
        """
        Schedule a periodic task using Celery Beat
        
        Args:
            task_name: Unique name for the task
            task_path: Python path to the task function
            schedule_type: 'interval', 'crontab', or 'solar'
            **schedule_kwargs: Schedule parameters
        """
        try:
            if schedule_type == 'interval':
                from celery.schedules import schedule
                schedule_obj = schedule(seconds=schedule_kwargs.get('seconds', 60))
            elif schedule_type == 'crontab':
                schedule_obj = crontab(
                    minute=schedule_kwargs.get('minute', '*'),
                    hour=schedule_kwargs.get('hour', '*'),
                    day_of_week=schedule_kwargs.get('day_of_week', '*'),
                    day_of_month=schedule_kwargs.get('day_of_month', '*'),
                    month_of_year=schedule_kwargs.get('month_of_year', '*')
                )
            else:
                raise ValueError(f"Unsupported schedule type: {schedule_type}")
            
            # Add to Celery beat schedule
            self.app.conf.beat_schedule[task_name] = {
                'task': task_path,
                'schedule': schedule_obj,
                'args': schedule_kwargs.get('args', ()),
                'kwargs': schedule_kwargs.get('kwargs', {})
            }
            
            logger.info(f"Scheduled Celery task '{task_name}' with {schedule_type} schedule")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling Celery task {task_name}: {str(e)}")
            return False


# Global scheduler instance
_scheduler_instance = None


def get_scheduler() -> SchedulerService:
    """Get the global scheduler instance"""
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = SchedulerService()
    return _scheduler_instance


# Convenience functions
def schedule_task(task_name: str, func: Callable, interval_seconds: int, *args, **kwargs) -> bool:
    """Schedule a recurring task"""
    scheduler = get_scheduler()
    return scheduler.schedule_task(task_name, func, interval_seconds, *args, **kwargs)


def schedule_daily_task(task_name: str, func: Callable, hour: int = 0, minute: int = 0, 
                       *args, **kwargs) -> bool:
    """Schedule a daily recurring task"""
    scheduler = get_scheduler()
    return scheduler.schedule_daily_task(task_name, func, hour, minute, *args, **kwargs)


def start_scheduler():
    """Start the global scheduler"""
    scheduler = get_scheduler()
    scheduler.start_scheduler()


def stop_scheduler():
    """Stop the global scheduler"""
    scheduler = get_scheduler()
    scheduler.stop_scheduler()
