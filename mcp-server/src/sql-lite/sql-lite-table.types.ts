/**
 * Base interface for database entities with auto-incrementing ID
 */
interface BaseEntity {
  id: number
}

/**
 * Interface for service-ninja-project table
 */
export interface ServiceNinjaProject extends BaseEntity {
  name: string
  description: string
}

/**
 * Interface for creating a new project (without ID)
 */
export interface CreateServiceNinjaProject {
  name: string
  description: string
}

/**
 * Interface for service-ninja-env table
 */
export interface ServiceNinjaEnv extends BaseEntity {
  name: string
  description?: string
  projectId: number
}

/**
 * Interface for creating a new environment (without ID)
 */
export interface CreateServiceNinjaEnv {
  name: string
  description?: string
  projectId: number
}

/**
 * Interface for service-ninja-resource table
 */
export interface ServiceNinjaResource extends BaseEntity {
  name: string
  description: string
  healthCheckUrl?: string
  aliveCheckUrl?: string
  headers?: string
  isIhService: boolean
  type: ServiceNinjaResourceType
  projectId: number
  envId: number
}

export enum ServiceNinjaResourceType {
  SERVICE = 'service',
  DATABASE = 'database',
  API = 'api',
  QUEUE = 'queue',
  CACHE = 'cache',
  STORAGE = 'storage',
}
/**
 * Interface for creating a new resource (without ID)
 */
export interface CreateServiceNinjaResource {
  name: string
  description: string
  healthCheckUrl?: string
  aliveCheckUrl?: string
  headers?: string
  isIhService?: boolean
  type: ServiceNinjaResourceType
  projectId: number
  envId: number
}

/**
 * Interface for service-ninja-contact table
 */
export interface ServiceNinjaContact extends BaseEntity {
  firstName: string
  lastName: string
  email: string
  phone?: string
}

/**
 * Interface for creating a new contact (without ID)
 */
export interface CreateServiceNinjaContact {
  firstName: string
  lastName: string
  email: string
  phone?: string
}

/**
 * Database query result types
 */
export type QueryResult<T> = T | null
export type QueryResults<T> = T[]

/**
 * Common query options
 */
export interface QueryOptions {
  limit?: number
  offset?: number
  orderBy?: string
  orderDirection?: 'ASC' | 'DESC'
}
