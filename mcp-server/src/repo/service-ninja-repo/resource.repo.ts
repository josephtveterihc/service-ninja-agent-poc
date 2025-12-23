import type { ServiceNinjaResource } from '../../sql-lite/sql-lite-table.types'
import { getOrCreateSqlLite } from '../../sql-lite/sql-lite.init'

const TABLE = '"service-ninja-resource"'
/**
 * Method: getServiceNinjaResources
 * Description: Retrieves Service Ninja resources from the database, optionally filtered by project and/or environment.
 * Arguments: Optional projectId and envId for filtering.
 * Returns: A promise that resolves to an array of ServiceNinjaResource.
 */
export async function getServiceNinjaResources(projectId?: number, envId?: number) {
  try {
    const db = await getOrCreateSqlLite()
    let sql = `SELECT * FROM ${TABLE}`
    const params = []

    if (projectId && envId) {
      sql += ` WHERE projectId = ? AND envId = ?`
      params.push(projectId, envId)
    } else if (projectId) {
      sql += ` WHERE projectId = ?`
      params.push(projectId)
    } else if (envId) {
      sql += ` WHERE envId = ?`
      params.push(envId)
    }

    const query = db.query(sql)
    const resources = query.all(...params) as ServiceNinjaResource[]
    return resources || []
  } catch (error) {
    console.error('--- getServiceNinjaResources error ---', error)
    throw new Error(`Failed to get resources: ${error}`)
  }
}

/**
 * Method: getServiceNinjaResource
 * Description: Retrieves a specific Service Ninja resource by name or ID.
 * Arguments: An object containing either the resource name or ID, and optionally projectId and envId.
 * Returns: A promise that resolves to the ServiceNinjaResource or undefined.
 */
export async function getServiceNinjaResource({
  name,
  id,
  projectId,
  envId,
}: {
  name?: string | undefined
  id?: number | undefined
  projectId?: number | undefined
  envId?: number | undefined
}) {
  try {
    if (!name && !id) {
      throw new Error('Either name or id must be provided')
    }
    const db = await getOrCreateSqlLite()

    let sql = `SELECT * FROM ${TABLE} WHERE ${name ? 'name = ?' : 'id = ?'}`
    const params = [name ?? id]

    if (projectId) {
      sql += ' AND projectId = ?'
      params.push(projectId)
    }
    if (envId) {
      sql += ' AND envId = ?'
      params.push(envId)
    }

    const query = db.query(sql)
    // @ts-ignore
    const resource = query.get(...params) as ServiceNinjaResource
    return resource
  } catch (error) {
    console.error('--- getServiceNinjaResource error ---', error)
    throw new Error(`Failed to get resource: ${error}`)
  }
}

/**
 * Method: createServiceNinjaResource
 * Description: Creates a new Service Ninja resource in the database.
 * Arguments: An object containing the resource details.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function createServiceNinjaResource(params: Partial<ServiceNinjaResource>): Promise<{ success: boolean }> {
  try {
    if (!params.name || !params.description || !params.type || !params.projectId || !params.envId) {
      throw new Error('Name, description, type, projectId, and envId are required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`
      INSERT INTO ${TABLE} 
      (name, description, type, projectId, envId, healthCheckUrl, aliveCheckUrl, headers, isIhService) 
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`)
    const result = query.run(
      params.name,
      params.description,
      params.type,
      params.projectId,
      params.envId,
      params.healthCheckUrl || null,
      params.aliveCheckUrl || null,
      params.headers || null,
      params.isIhService || false
    )

    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to create resource: ${error}`)
  }
}

/**
 * Method: updateServiceNinjaResource
 * Description: Updates an existing Service Ninja resource in the database.
 * Arguments: An object containing the resource ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaResource(params: Partial<ServiceNinjaResource> & { id: number }): Promise<{ success: boolean }> {
  try {
    if (!params.id) {
      throw new Error('Resource ID is required for update')
    }

    const db = await getOrCreateSqlLite()
    const fieldsToUpdate = []
    const values = []

    if (params.name) {
      fieldsToUpdate.push('name = ?')
      values.push(params.name)
    }
    if (params.description !== undefined) {
      fieldsToUpdate.push('description = ?')
      values.push(params.description)
    }
    if (params.type) {
      fieldsToUpdate.push('type = ?')
      values.push(params.type)
    }
    if (params.projectId) {
      fieldsToUpdate.push('projectId = ?')
      values.push(params.projectId)
    }
    if (params.envId) {
      fieldsToUpdate.push('envId = ?')
      values.push(params.envId)
    }
    if (params.healthCheckUrl !== undefined) {
      fieldsToUpdate.push('healthCheckUrl = ?')
      values.push(params.healthCheckUrl)
    }
    if (params.aliveCheckUrl !== undefined) {
      fieldsToUpdate.push('aliveCheckUrl = ?')
      values.push(params.aliveCheckUrl)
    }
    if (params.headers !== undefined) {
      fieldsToUpdate.push('headers = ?')
      values.push(params.headers)
    }
    if (params.isIhService !== undefined) {
      fieldsToUpdate.push('isIhService = ?')
      values.push(params.isIhService)
    }

    if (fieldsToUpdate.length === 0) {
      throw new Error('No fields to update')
    }

    values.push(params.id) // ID for WHERE clause

    const sql = `UPDATE ${TABLE} SET ${fieldsToUpdate.join(', ')} WHERE id = ?`
    const query = db.query(sql)
    const result = query.run(...values)
    return { success: result.changes > 0 }
  } catch (error) {
    console.error('--- updateServiceNinjaResource error ---', error)
    throw new Error(`Failed to update resource: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaResource
 * Description: Deletes a Service Ninja resource from the database.
 * Arguments: The resource ID to delete.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaResource(id: number): Promise<{ success: boolean }> {
  try {
    if (!id) {
      throw new Error('Resource ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM ${TABLE} WHERE id = ?`)
    const result = query.run(id)
    return { success: result.changes > 0 }
  } catch (error) {
    console.error('--- deleteServiceNinjaResource error ---', error)
    throw new Error(`Failed to delete resource: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaResourcesByEnvId
 * Description: Deletes all Service Ninja resources for a specific environment.
 * Arguments: The environment ID to delete resources for.
 * Returns: A promise that resolves to an object indicating success and number of deleted records.
 */
export async function deleteServiceNinjaResourcesByEnvId(envId: number): Promise<{ success: boolean; deletedCount: number }> {
  try {
    if (!envId) {
      throw new Error('Environment ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM ${TABLE} WHERE envId = ?`)
    const result = query.run(envId)
    return { success: true, deletedCount: result.changes }
  } catch (error) {
    console.error('--- deleteServiceNinjaResourcesByEnvId error ---', error)
    throw new Error(`Failed to delete resources for environment: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaResourcesByProjectId
 * Description: Deletes all Service Ninja resources for a specific project.
 * Arguments: The project ID to delete resources for.
 * Returns: A promise that resolves to an object indicating success and number of deleted records.
 */
export async function deleteServiceNinjaResourcesByProjectId(projectId: number): Promise<{ success: boolean; deletedCount: number }> {
  try {
    if (!projectId) {
      throw new Error('Project ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM ${TABLE} WHERE projectId = ?`)
    const result = query.run(projectId)
    return { success: true, deletedCount: result.changes }
  } catch (error) {
    throw new Error(`Failed to delete resources for project: ${error}`)
  }
}
