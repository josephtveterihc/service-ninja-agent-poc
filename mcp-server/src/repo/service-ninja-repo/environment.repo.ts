import type { ServiceNinjaEnv } from '../../sql-lite/sql-lite-table.types'
import { getOrCreateSqlLite } from '../../sql-lite/sql-lite.init'

/**
 * Method: getServiceNinjaEnvs
 * Description: Retrieves all Service Ninja environments from the database.
 * Arguments: Optional projectId for filtering.
 * Returns: A promise that resolves to an array of ServiceNinjaEnv.
 */
export async function getServiceNinjaEnvs(projectId?: number) {
  try {
    const db = await getOrCreateSqlLite()
    let sql = `SELECT * FROM "service-ninja-env"`
    const params = []

    if (projectId) {
      sql += ` WHERE projectId = ?`
      params.push(projectId)
    }

    const query = db.query(sql)
    const envs = query.all(...params) as ServiceNinjaEnv[]
    return envs || []
  } catch (error) {
    throw new Error(`Failed to get environments: ${error}`)
  }
}

/**
 * Method: getServiceNinjaEnv
 * Description: Retrieves a specific Service Ninja environment by name or ID.
 * Arguments: An object containing either the environment name or ID, and optionally projectId.
 * Returns: A promise that resolves to the ServiceNinjaEnv or undefined.
 */
export async function getServiceNinjaEnv({ name, id, projectId }: { name?: string | undefined; id?: number | undefined; projectId?: number | undefined }) {
  try {
    if (!name && !id) {
      throw new Error('Either name or id must be provided')
    }
    const db = await getOrCreateSqlLite()

    let sql = `SELECT * FROM "service-ninja-env" WHERE ${name ? 'name = ?' : 'id = ?'}`
    const params = [name ?? id]

    if (projectId) {
      sql += ' AND projectId = ?'
      params.push(projectId)
    }

    const query = db.query(sql)
    // @ts-ignore
    const env = query.get(...params) as ServiceNinjaEnv
    return env
  } catch (error) {
    throw new Error(`Failed to get environment: ${error}`)
  }
}

/**
 * Method: createServiceNinjaEnv
 * Description: Creates a new Service Ninja environment in the database.
 * Arguments: An object containing the environment name, description, and projectId.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function createServiceNinjaEnv(params: { name: string | undefined; description?: string | undefined; projectId: number | undefined }): Promise<{ success: boolean }> {
  try {
    if (!params.name || !params.projectId) {
      throw new Error('Environment name and projectId are required')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`INSERT INTO "service-ninja-env" (name, description, projectId) VALUES (?, ?, ?)`)
    const result = query.run(params.name, params.description || '', params.projectId)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to create environment: ${error}`)
  }
}

/**
 * Method: updateServiceNinjaEnv
 * Description: Updates an existing Service Ninja environment in the database.
 * Arguments: An object containing the environment ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaEnv(params: Partial<ServiceNinjaEnv> & { id: number }): Promise<{ success: boolean }> {
  try {
    if (!params.id) {
      throw new Error('Environment ID is required for update')
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
    if (params.projectId) {
      fieldsToUpdate.push('projectId = ?')
      values.push(params.projectId)
    }

    if (fieldsToUpdate.length === 0) {
      throw new Error('No fields to update')
    }

    values.push(params.id) // ID for WHERE clause

    const sql = `UPDATE "service-ninja-env" SET ${fieldsToUpdate.join(', ')} WHERE id = ?`
    const query = db.query(sql)
    const result = query.run(...values)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to update environment: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaEnv
 * Description: Deletes a Service Ninja environment from the database.
 * Arguments: The environment ID to delete.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaEnv(id: number): Promise<{ success: boolean }> {
  try {
    if (!id) {
      throw new Error('Environment ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "service-ninja-env" WHERE id = ?`)
    const result = query.run(id)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to delete environment: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaEnvsByProjectId
 * Description: Deletes all Service Ninja environments for a specific project.
 * Arguments: The project ID to delete environments for.
 * Returns: A promise that resolves to an object indicating success and number of deleted records.
 */
export async function deleteServiceNinjaEnvsByProjectId(projectId: number): Promise<{ success: boolean; deletedCount: number }> {
  try {
    if (!projectId) {
      throw new Error('Project ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "service-ninja-env" WHERE projectId = ?`)
    const result = query.run(projectId)
    return { success: true, deletedCount: result.changes }
  } catch (error) {
    throw new Error(`Failed to delete environments for project: ${error}`)
  }
}
