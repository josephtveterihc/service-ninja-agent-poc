import type { CreateServiceNinjaContact, ServiceNinjaContact } from '../../sql-lite/sql-lite-table.types'
import { getOrCreateSqlLite } from '../../sql-lite/sql-lite.init'

/**
 * Method: getServiceNinjaContacts
 * Description: Retrieves all Service Ninja contacts from the database.
 * Returns: A promise that resolves to an array of ServiceNinjaContact.
 */
export async function getServiceNinjaContacts() {
  try {
    const db = await getOrCreateSqlLite()
    const query = db.query(`SELECT * FROM "service-ninja-contact"`)
    const contacts = query.all() as ServiceNinjaContact[]
    return contacts || []
  } catch (error) {
    throw new Error(`Failed to get contacts: ${error}`)
  }
}

/**
 * Method: getServiceNinjaContact
 * Description: Retrieves a specific Service Ninja contact by email or ID.
 * Arguments: An object containing either the contact email or ID.
 * Returns: A promise that resolves to the ServiceNinjaContact or undefined.
 */
export async function getServiceNinjaContact({ email, id }: { email?: string | undefined; id?: number | undefined }) {
  try {
    if (!email && !id) {
      throw new Error('Either email or id must be provided')
    }
    const db = await getOrCreateSqlLite()
    const sql = `SELECT * FROM "service-ninja-contact" WHERE ${email ? 'email = ?' : 'id = ?'}`
    const query = db.query(sql)
    const key = email ? email : id!
    const contact = query.get(key) as ServiceNinjaContact
    return contact
  } catch (error) {
    throw new Error(`Failed to get contact: ${error}`)
  }
}

/**
 * Method: createServiceNinjaContact
 * Description: Creates a new Service Ninja contact in the database.
 * Arguments: An object containing the contact details.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function createServiceNinjaContact(params: CreateServiceNinjaContact): Promise<{ success: boolean }> {
  try {
    if (!params.firstName || !params.lastName || !params.email) {
      throw new Error('First name, last name, and email are required')
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(params.email)) {
      throw new Error('Invalid email format')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`
      INSERT INTO "service-ninja-contact" (firstName, lastName, email, phone) 
      VALUES (?, ?, ?, ?)
    `)

    const result = query.run(params.firstName, params.lastName, params.email, params.phone || null)

    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to create contact: ${error}`)
  }
}

/**
 * Method: updateServiceNinjaContact
 * Description: Updates an existing Service Ninja contact in the database.
 * Arguments: An object containing the contact ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaContact(params: Partial<ServiceNinjaContact> & { id: number }): Promise<{ success: boolean }> {
  try {
    if (!params.id) {
      throw new Error('Contact ID is required for update')
    }

    const db = await getOrCreateSqlLite()
    const fieldsToUpdate = []
    const values = []

    if (params.firstName) {
      fieldsToUpdate.push('firstName = ?')
      values.push(params.firstName)
    }
    if (params.lastName) {
      fieldsToUpdate.push('lastName = ?')
      values.push(params.lastName)
    }
    if (params.email) {
      // Basic email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(params.email)) {
        throw new Error('Invalid email format')
      }
      fieldsToUpdate.push('email = ?')
      values.push(params.email)
    }
    if (params.phone !== undefined) {
      fieldsToUpdate.push('phone = ?')
      values.push(params.phone)
    }

    if (fieldsToUpdate.length === 0) {
      throw new Error('No fields to update')
    }

    values.push(params.id) // ID for WHERE clause

    const sql = `UPDATE "service-ninja-contact" SET ${fieldsToUpdate.join(', ')} WHERE id = ?`
    const query = db.query(sql)
    const result = query.run(...values)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to update contact: ${error}`)
  }
}

/**
 * Method: deleteServiceNinjaContact
 * Description: Deletes a Service Ninja contact from the database.
 * Arguments: The contact ID to delete.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaContact(id: number): Promise<{ success: boolean }> {
  try {
    if (!id) {
      throw new Error('Contact ID is required for deletion')
    }
    const db = await getOrCreateSqlLite()
    const query = db.query(`DELETE FROM "service-ninja-contact" WHERE id = ?`)
    const result = query.run(id)
    return { success: result.changes > 0 }
  } catch (error) {
    throw new Error(`Failed to delete contact: ${error}`)
  }
}

/**
 * Method: searchServiceNinjaContacts
 * Description: Searches Service Ninja contacts by name or email.
 * Arguments: A search term to match against firstName, lastName, or email.
 * Returns: A promise that resolves to an array of matching ServiceNinjaContact.
 */
export async function searchServiceNinjaContacts(searchTerm: string) {
  try {
    if (!searchTerm || searchTerm.trim().length === 0) {
      throw new Error('Search term is required')
    }

    const db = await getOrCreateSqlLite()
    const query = db.query(`
      SELECT * FROM "service-ninja-contact" 
      WHERE firstName LIKE ? OR lastName LIKE ? OR email LIKE ?
      ORDER BY lastName, firstName
    `)

    const likeTerm = `%${searchTerm.trim()}%`
    const contacts = query.all(likeTerm, likeTerm, likeTerm) as ServiceNinjaContact[]
    return contacts || []
  } catch (error) {
    throw new Error(`Failed to search contacts: ${error}`)
  }
}
