import type { ServiceNinjaResourceContact } from '../../sql-lite/sql-lite-table.types'
import { getOrCreateSqlLite } from '../../sql-lite/sql-lite.init'

const TABLE = 'service-ninja-resource-contact'
/**
 * Method: getResourceContacts
 * Description: Retrieves all resource-contact associations from the database.
 * Returns: A promise that resolves to an array of ServiceNinjaResourceContact.
 */
export async function getResourceContacts() {
  try {
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM "${TABLE}"`)
    const resourceContacts = query.all() as ServiceNinjaResourceContact[]
    return resourceContacts || []
  } catch (error) {
    throw new Error(`Failed to get resource contacts: ${error}`)
  }
}

/**
 * Method: getResourceContactsByResourceId
 * Description: Retrieves all contacts for a specific resource.
 * Arguments: The resource ID.
 * Returns: A promise that resolves to an array of ServiceNinjaResourceContact.
 */
export async function getResourceContactsByResourceId(resourceId: number) {
  try {
    if (!resourceId) {
      throw new Error('Resource ID is required')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM "${TABLE}" WHERE resourceId = ?`)
    const resourceContacts = query.all(resourceId) as ServiceNinjaResourceContact[]
    return resourceContacts || []
  } catch (error) {
    throw new Error(`Failed to get resource contacts: ${error}`)
  }
}

/**
 * Method: getResourceContactsByContactId
 * Description: Retrieves all resources for a specific contact.
 * Arguments: The contact ID.
 * Returns: A promise that resolves to an array of ServiceNinjaResourceContact.
 */
export async function getResourceContactsByContactId(contactId: number) {
  try {
    if (!contactId) {
      throw new Error('Contact ID is required')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM "${TABLE}" WHERE contactId = ?`)
    const resourceContacts = query.all(contactId) as ServiceNinjaResourceContact[]
    return resourceContacts || []
  } catch (error) {
    throw new Error(`Failed to get resource contacts: ${error}`)
  }
}

/**
 * Method: getResourceContact
 * Description: Retrieves a specific resource-contact association.
 * Arguments: An object containing the resource ID and contact ID.
 * Returns: A promise that resolves to the ServiceNinjaResourceContact or undefined.
 */
export async function getResourceContact({ resourceId, contactId }: { resourceId: number; contactId: number }) {
  try {
    if (!resourceId || !contactId) {
      throw new Error('Both resource ID and contact ID are required')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM "${TABLE}" WHERE resourceId = ? AND contactId = ?`)
    const resourceContact = query.get(resourceId, contactId) as ServiceNinjaResourceContact
    return resourceContact
  } catch (error) {
    throw new Error(`Failed to get resource contact: ${error}`)
  }
}

/**
 * Method: createResourceContact
 * Description: Creates a new resource-contact association in the database.
 * Arguments: An object containing the resource ID, contact ID, and role.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function createResourceContact(params: ServiceNinjaResourceContact): Promise<{ success: boolean }> {
  try {
    if (!params.resourceId || !params.contactId || !params.role) {
      throw new Error('Resource ID, contact ID, and role are required')
    }

    // Check if association already exists
    const existing = await getResourceContact({ resourceId: params.resourceId, contactId: params.contactId })
    if (existing) {
      throw new Error('Resource-contact association already exists')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`
      INSERT INTO "${TABLE}" (resourceId, contactId, role) 
      VALUES (?, ?, ?)
    `)

    const result = query.run(params.resourceId, params.contactId, params.role)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to create resource contact: ${error}`)
  }
}

/**
 * Method: updateResourceContact
 * Description: Updates an existing resource-contact association in the database.
 * Arguments: An object containing the resource ID, contact ID, and new role.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateResourceContact(params: { resourceId: number; contactId: number; role: string }): Promise<{ success: boolean }> {
  try {
    if (!params.resourceId || !params.contactId || !params.role) {
      throw new Error('Resource ID, contact ID, and role are required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`
      UPDATE "${TABLE}" 
      SET role = ? 
      WHERE resourceId = ? AND contactId = ?`)

    const result = query.run(params.role, params.resourceId, params.contactId)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to update resource contact: ${error}`)
  }
}

/**
 * Method: deleteResourceContact
 * Description: Deletes a resource-contact association from the database.
 * Arguments: An object containing the resource ID and contact ID.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteResourceContact({ resourceId, contactId }: { resourceId: number; contactId: number }): Promise<{ success: boolean }> {
  try {
    if (!resourceId || !contactId) {
      throw new Error('Both resource ID and contact ID are required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "${TABLE}" WHERE resourceId = ? AND contactId = ?`)
    const result = query.run(resourceId, contactId)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to delete resource contact: ${error}`)
  }
}

/**
 * Method: deleteResourceContactsByResourceId
 * Description: Deletes all contact associations for a specific resource.
 * Arguments: The resource ID.
 * Returns: A promise that resolves to an object indicating success and count of deleted records.
 */
export async function deleteResourceContactsByResourceId(resourceId: number): Promise<{ success: boolean; deletedCount: number }> {
  try {
    if (!resourceId) {
      throw new Error('Resource ID is required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "${TABLE}" WHERE resourceId = ?`)
    const result = query.run(resourceId)
    return { success: result.changes > 0, deletedCount: result.changes }
  } catch (error) {
    throw new Error(`Failed to delete resource contacts: ${error}`)
  }
}

/**
 * Method: deleteResourceContactsByContactId
 * Description: Deletes all resource associations for a specific contact.
 * Arguments: The contact ID.
 * Returns: A promise that resolves to an object indicating success and count of deleted records.
 */
export async function deleteResourceContactsByContactId(contactId: number): Promise<{ success: boolean; deletedCount: number }> {
  try {
    if (!contactId) {
      throw new Error('Contact ID is required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "${TABLE}" WHERE contactId = ?`)
    const result = query.run(contactId)
    return { success: result.changes > 0, deletedCount: result.changes }
  } catch (error) {
    throw new Error(`Failed to delete resource contacts: ${error}`)
  }
}

/**
 * Method: getResourceContactsWithDetails
 * Description: Retrieves resource-contact associations with full resource and contact details.
 * Arguments: Optional resource ID to filter by specific resource.
 * Returns: A promise that resolves to an array of detailed resource-contact information.
 */
export async function getResourceContactsWithDetails(resourceId?: number) {
  try {
    const db = await getOrCreateSqlLite()
    let sql = `
      SELECT 
        rc.resourceId,
        rc.contactId,
        rc.role,
        r.name as resourceName,
        r.description as resourceDescription,
        r.type as resourceType,
        c.firstName,
        c.lastName,
        c.email,
        c.phone
      FROM "${TABLE}" rc
      JOIN "service-ninja-resource" r ON rc.resourceId = r.id
      JOIN "service-ninja-contact" c ON rc.contactId = c.id
    `

    const params: any[] = []
    if (resourceId) {
      sql += ` WHERE rc.resourceId = ?`
      params.push(resourceId)
    }

    sql += ` ORDER BY r.name, c.lastName, c.firstName`

    const query = db.query(sql)
    const results = params.length > 0 ? query.all(...params) : query.all()
    return results || []
  } catch (error) {
    throw new Error(`Failed to get resource contacts with details: ${error}`)
  }
}
