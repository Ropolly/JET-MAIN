/**
 * Haversine formula to calculate the great circle distance between two points 
 * on the earth (specified in decimal degrees)
 * 
 * @param lat1 Latitude of first point in decimal degrees
 * @param lon1 Longitude of first point in decimal degrees
 * @param lat2 Latitude of second point in decimal degrees
 * @param lon2 Longitude of second point in decimal degrees
 * @returns Distance in nautical miles
 */
export function calculateDistance(lat1: number, lon1: number, lat2: number, lon2: number): number {
  // Convert decimal degrees to radians
  const lat1Rad = toRadians(lat1);
  const lon1Rad = toRadians(lon1);
  const lat2Rad = toRadians(lat2);
  const lon2Rad = toRadians(lon2);

  // Haversine formula
  const dLat = lat2Rad - lat1Rad;
  const dLon = lon2Rad - lon1Rad;
  
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1Rad) * Math.cos(lat2Rad) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  
  // Radius of Earth in kilometers
  const earthRadiusKm = 6371;
  const distanceKm = earthRadiusKm * c;
  
  // Convert kilometers to nautical miles (1 km = 0.539957 nautical miles)
  const distanceNm = distanceKm * 0.539957;
  
  return Math.round(distanceNm * 10) / 10; // Round to 1 decimal place
}

/**
 * Calculate distance between two airports using their coordinates
 * 
 * @param airport1 Airport object with latitude and longitude
 * @param airport2 Airport object with latitude and longitude
 * @returns Distance in nautical miles, or null if coordinates are missing
 */
export function calculateAirportDistance(airport1: any, airport2: any): number | null {
  if (!airport1?.latitude || !airport1?.longitude || !airport2?.latitude || !airport2?.longitude) {
    return null;
  }

  return calculateDistance(
    parseFloat(airport1.latitude),
    parseFloat(airport1.longitude),
    parseFloat(airport2.latitude),
    parseFloat(airport2.longitude)
  );
}

/**
 * Calculate total distance for a trip with multiple legs
 * 
 * @param tripLines Array of trip line objects with origin_airport and destination_airport
 * @returns Total distance in nautical miles
 */
export function calculateTripDistance(tripLines: any[]): number {
  if (!tripLines || tripLines.length === 0) {
    return 0;
  }

  let totalDistance = 0;

  for (const line of tripLines) {
    if (line.origin_airport && line.destination_airport) {
      const distance = calculateAirportDistance(line.origin_airport, line.destination_airport);
      if (distance !== null) {
        totalDistance += distance;
      }
    }
  }

  return Math.round(totalDistance * 10) / 10; // Round to 1 decimal place
}

/**
 * Convert degrees to radians
 */
function toRadians(degrees: number): number {
  return degrees * (Math.PI / 180);
}

/**
 * Calculate estimated flight time based on distance
 * Uses average cruise speed of 400 knots for jets
 * 
 * @param distanceNm Distance in nautical miles
 * @param cruiseSpeedKnots Average cruise speed in knots (default: 400)
 * @returns Flight time in hours (decimal)
 */
export function calculateFlightTime(distanceNm: number, cruiseSpeedKnots: number = 400): number {
  if (!distanceNm || distanceNm <= 0) {
    return 0;
  }

  const flightTimeHours = distanceNm / cruiseSpeedKnots;
  return Math.round(flightTimeHours * 10) / 10; // Round to 1 decimal place
}

/**
 * Calculate flight time between two airports
 * 
 * @param airport1 Origin airport with coordinates
 * @param airport2 Destination airport with coordinates
 * @param cruiseSpeedKnots Average cruise speed in knots (default: 400)
 * @returns Flight time in hours, or null if coordinates missing
 */
export function calculateAirportFlightTime(airport1: any, airport2: any, cruiseSpeedKnots: number = 400): number | null {
  const distance = calculateAirportDistance(airport1, airport2);
  if (distance === null) {
    return null;
  }
  
  return calculateFlightTime(distance, cruiseSpeedKnots);
}

/**
 * Format distance for display
 * 
 * @param distance Distance in nautical miles
 * @param showUnits Whether to include "nm" suffix
 * @returns Formatted distance string
 */
export function formatDistance(distance: number | null, showUnits: boolean = true): string {
  if (distance === null || distance === 0) {
    return 'TBD';
  }

  const formatted = distance.toLocaleString();
  return showUnits ? `${formatted} nm` : formatted;
}