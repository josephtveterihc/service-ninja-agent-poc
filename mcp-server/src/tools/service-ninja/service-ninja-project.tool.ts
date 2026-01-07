import { createServiceNinjaProject, deleteServiceNinjaProject, getServiceNinjaProject, getServiceNinjaProjects, updateServiceNinjaProject } from '../../repo/service-ninja-repo'
import type { ServiceNinjaProject } from '../../sql-lite/sql-lite-table.types'
import type { McpToolCallResult } from '../../types'

export async function createServiceNinjaProjectTool(args: { name: string; description: string }): Promise<McpToolCallResult> {
  console.log('--- createServiceNinjaProjectTool --- args:', args)
  const { name, description } = args
  const projects = await getServiceNinjaProjects()
  const existingProject = await projects.find((project: { name: string }) => project.name.toLowerCase() === name.toLowerCase())

  if (existingProject) {
    console.log('--- Project already exists ---')
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Project with name "${name}" already exists.`,
        },
      ],
    }
  }
  const res = await createServiceNinjaProject({ name, description })

  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: `Project "${name}" created successfully with ID ${res.success}.`,
      },
    ],
  }
}
/**
 * Method: readServiceNinjaProjectTool
 * Description: Retrieves a specific Service Ninja project by name or ID.
 * Arguments: An object containing either the project name or ID.
 * Returns: A promise that resolves to an McpToolCallResult containing the project details.
 */
export async function readServiceNinjaProjectTool({ name, id }: { name?: string; id?: number }): Promise<McpToolCallResult> {
  // This shold be implemented to read a specific project by ID or name
  const project = await getServiceNinjaProject({ name, id })

  if (!project) {
    return {
      isError: true,
      content: [
        {
          type: 'text',
          text: `Project not found.`,
        },
      ],
    }
  }

  return {
    isError: false,
    content: [
      {
        type: 'text',
        data: JSON.stringify({ project }),
        text: `Project details retrieved successfully.`,
      },
    ],
  }
}

/**
 * Method: updateServiceNinjaProjectTool
 * Description: Updates an existing Service Ninja project.
 * Arguments: An object containing the project ID, name, and/or description.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function updateServiceNinjaProjectTool(params: Partial<ServiceNinjaProject>): Promise<McpToolCallResult> {
  console.log('--- updateServiceNinjaProjectTool --- params:', params)
  // TODO - Handle Throw
  await updateServiceNinjaProject(params)
  return { isError: false, content: [{ type: 'text', text: `Project updated successfully.` }] }
}

/**
 * Method: deleteServiceNinjaProjectTool
 * Description: Deletes a specific Service Ninja project by ID.
 * Arguments: An object containing the project ID.
 * Returns: A promise that resolves to an object indicating success.
 */
export async function deleteServiceNinjaProjectTool(params: { id: number }): Promise<McpToolCallResult> {
  console.log('--- deleteServiceNinjaProjectTool --- params:', params)
  // TODO - Handle Throw
  await deleteServiceNinjaProject(params.id)
  return { isError: false, content: [{ type: 'text', text: `Project deleted successfully.` }] }
}

/**
 * Method: getProjectToolListTool
 * Description: Retrieves the list of Service Ninja projects from the database.
 * Arguments: None
 * Returns: A promise that resolves to an McpToolCallResult containing the list of projects.
 */
export async function getProjectToolListTool(): Promise<McpToolCallResult> {
  console.log('--- getProjectToolListTool ---')
  const projects = await getServiceNinjaProjects()
  return {
    isError: false,
    content: [
      {
        type: 'text',
        text: JSON.stringify({ projects }),
        // text: `Project list retrieved successfully.`,
      },
    ],
  }
}
