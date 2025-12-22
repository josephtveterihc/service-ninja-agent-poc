import { Database } from 'bun:sqlite'
import path from 'path'

// https://www.sqlite.org/autoinc.html

let db: Database
const createServiceNinjaProjectTable = `
CREATE TABLE IF NOT EXISTS 'service-ninja-project' (
	id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
	description TEXT NOT NULL
);
`

const createServiceNinjaEnvTable = `
CREATE TABLE IF NOT EXISTS "service-ninja-env" (
	id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
	description TEXT,
  projectId INTEGER NOT NULL
);
`

const createServiceNinjaResourceTable = `
CREATE TABLE IF NOT EXISTS "service-ninja-resource" (
	id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
	description TEXT NOT NULL,
  healthCheckUrl TEXT,
  aliveCheckUrl TEXT,
  headers TEXT,
  isIhService BOOLEAN DEFAULT false,
  type TEXT NOT NULL, 
  projectId INTEGER NOT NULL,
  envId INTEGER NOT NULL
);
`

const createContactTable = `
CREATE TABLE IF NOT EXISTS "service-ninja-contact" (
  id INTEGER PRIMARY KEY,
  firstName TEXT NOT NULL,
  lastName TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT
);
`

/**
 * Method: getOrCreateSqlLite
 * Description: Initializes and returns the SQLite database instance.
 * Returns: A promise that resolves to the Database instance.
 */
export async function getOrCreateSqlLite() {
  try {
    if (db) {
      console.log('has DB instance')
      return db
    }
    const dbPath = path.join(process.cwd(), 'mcp.sqlite')
    console.log('dbPath', dbPath)
    db = await new Database(dbPath, { create: true })
    if (db) {
      console.log('DB instance created')
      const projectQuery = db.query(createServiceNinjaProjectTable)
      const envQuery = db.query(createServiceNinjaEnvTable)
      const resourceQuery = db.query(createServiceNinjaResourceTable)
      const contactQuery = db.query(createContactTable)

      projectQuery.run()
      envQuery.run()
      resourceQuery.run()
      contactQuery.run()
    }

    return db
  } catch (err) {
    console.error(`Failed to get database`, { err })
    throw new Error('Failed to get database')
  }
}
