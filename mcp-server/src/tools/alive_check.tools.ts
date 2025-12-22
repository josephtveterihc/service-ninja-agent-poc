export interface AliveCheckResponse {}
export function serviceCheckAlive(): Promise<AliveCheckResponse> {
  // TODO: Implement actual alive check logic
  // use axios or fetch to call an internal endpoint or perform necessary checks
  // Find the URL and headers from project info
  return Promise.resolve({})
}
