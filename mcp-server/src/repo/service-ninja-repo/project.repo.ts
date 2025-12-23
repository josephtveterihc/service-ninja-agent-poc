import type { ServiceNinjaProject } from '../../sql-lite/sql-lite-table.types'
import { getOrCreateSqlLite } from '../../sql-lite/sql-lite.init'

const TABLE = '"service-ninja-project"'
/**
 * Method: getServiceNinjaProjects
 * Description: Retrieves all Service Ninja projects from the database.
 * Returns: A promise that resolves to an array of ServiceNinjaProject.
 */
export async function getServiceNinjaProjects() {
  try {
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM ${TABLE}`)
    const projects = query.all() as ServiceNinjaProject[]
    return projects || []
  } catch (error) {
    throw new Error(`Failed to get projects: ${error}`)
  }
}

/**
 * Method: getServiceNinjaProject
 * Description: Retrieves a specific Service Ninja project by name or ID.
 * Arguments: An object containing either the project name or ID.
 * Returns: A promise that resolves to the ServiceNinjaProject or undefined.
 */
export async function getServiceNinjaProject({ name, id }: { name?: string | undefined; id?: number | undefined }) {
  try {
    if (!name && !id) {
      throw new Error('Either name or id must be provided')
    }
    const db = await getOrCreateSqlLite()
    const sql = `SELECT * FROM ${TABLE} WHERE ${name ? 'name = ?' : 'id = ?'}`
    const query = db.query(sql)
    const key = name ?? (id as string | number)
    const project = query.get(key) as ServiceNinjaProject
    return project
  } catch (error) {
    throw new Error(`Failed to get project: ${error}`)
  }
}

/**
 * Method: createServiceNinjaProject
 * Description: Creates a new Service Ninja project in the database.
 * Arguments: An object containing the project name and description.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function createServiceNinjaProject(params: { name: string; description: string }): Promise<{ success: boolean }> {
  console.log('--- createServiceNinjaProject --- params:', params)
  try {
    if (!params.name || !params.description) {
      throw new Error('Project name and description are required')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`INSERT INTO ${TABLE} (name, description) VALUES (?, ?)`)
    const result = query.run(params.name, params.description)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to create project: ${error}`)
  }
}

/**
 * Method: updateServiceNinjaProject
 * Description: Updates an existing Service Ninja project in the database.
 * Arguments: An object containing the project ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaProject(params: Partial<ServiceNinjaProject>): Promise<{ success: boolean }> {
  try {
    if (!params.id) {
      throw new Error('Project ID is required for update')
    }
    const db = await getOrCreateSqlLite()
    const fieldsToUpdate = []
    const values = []

    if (params.name) {
      fieldsToUpdate.push('name = ?')
      values.push(params.name)
    }
    if (params.description) {
      fieldsToUpdate.push('description = ?')
      values.push(params.description)
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
    throw new Error(`Failed to update project: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaProject
 * Description: Deletes a Service Ninja project from the database.
 * Arguments: The project ID to delete.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaProject(id: number): Promise<{ success: boolean }> {
  try {
    if (!id) {
      throw new Error('Project ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM ${TABLE} WHERE id = ?`)
    const result = query.run(id)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to delete project: ${error}`)
  }
}
