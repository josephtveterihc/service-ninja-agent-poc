import { createServiceNinjaEnv, deleteServiceNinjaEnv, getServiceNinjaEnv, getServiceNinjaEnvs, updateServiceNinjaEnv } from '../../repo/service-ninja-repo'
import type { ServiceNinjaEnv } from '../../sql-lite/sql-lite-table.types'
import type { McpToolCallResult } from '../../types'

export async function createServiceNinjaEnvironmentTool(args: Partial<ServiceNinjaEnv>): Promise<McpToolCallResult> {
  console.log('--- createServiceNinjaEnvironmentTool --- args:', args)
  const { name, description, projectId } = args
  const environments = await getServiceNinjaEnvs(projectId)
  const existingEnvironment = environments.find((env: { name: string }) => env.name.toLowerCase() === name?.toLowerCase())

  if (existingEnvironment) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Environment with name "${name}" already exists in this project.`,
        },
      ],
    }
  }
  const res = await createServiceNinjaEnv({ name, description, projectId })

  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: `Environment "${name}" created successfully with ID ${res.success}.`,
      },
    ],
  }
}

/**
 * Method: readServiceNinjaEnvironmentTool
 * Description: Retrieves a specific Service Ninja environment by name or ID.
 * Arguments: An object containing either the environment name or ID, and optionally projectId.
 * Returns: A promise that resolves to an McpToolCallResult containing the environment details.
 */
export async function readServiceNinjaEnvironmentTool({ name, id, projectId }: { name?: string; id?: number; projectId?: number }): Promise<McpToolCallResult> {
  const environment = await getServiceNinjaEnv({ name, id, projectId })

  if (!environment) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Environment not found.`,
        },
      ],
    }
  }

  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: JSON.stringify({ environment }),
      },
    ],
  }
}

/**
 * Method: updateServiceNinjaEnvironmentTool
 * Description: Updates an existing Service Ninja environment.
 * Arguments: An object containing the environment ID and fields to update.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaEnvironmentTool(params: Partial<ServiceNinjaEnv> & { id: number }): Promise<McpToolCallResult> {
  console.log('--- updateServiceNinjaEnvironmentTool --- params:', params)
  // TODO - Handle Throw
  await updateServiceNinjaEnv(params)
  return { isError: false, content: [{ type: 'text', text: `Environment updated successfully.` }] }
}

/**
 * Method: deleteServiceNinjaEnvironmentTool
 * Description: Deletes a specific Service Ninja environment by ID.
 * Arguments: An object containing the environment ID.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaEnvironmentTool(params: { id: number }): Promise<McpToolCallResult> {
  console.log('--- deleteServiceNinjaEnvironmentTool --- params:', params)
  // TODO - Handle Throw
  await deleteServiceNinjaEnv(params.id)
  return { isError: false, content: [{ type: 'text', text: `Environment deleted successfully.` }] }
}

/**
 * Method: getEnvironmentToolListTool
 * Description: Retrieves the list of Service Ninja environments from the database, optionally filtered by project.
 * Arguments: Optional projectId for filtering.
 * Returns: A promise that resolves to an McpToolCallResult containing the list of environments.
 */
export async function getEnvironmentToolListTool(projectId?: number): Promise<McpToolCallResult> {
  console.log('--- getEnvironmentToolListTool --- projectId:', projectId)
  const environments = await getServiceNinjaEnvs(projectId)
  console.log('--- Environments retrieved:', environments)
  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: JSON.stringify({ environments }),
      },
    ],
  }
}
