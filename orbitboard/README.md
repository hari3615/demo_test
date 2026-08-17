# Orbitboard

Orbitboard is a team task and project tracker backend designed to help you organize workflows, track effort estimates, and collaborate efficiently.

## Features

- **Project Management**: Create and manage projects.
- **Task Tracking**: Assign tasks, track status (TODO, IN_PROGRESS, DONE), and estimate effort.
- **Due Date Recomputation**: Automatically update due dates based on effort estimates.
- **Comments & Notifications**: Discuss tasks in comments and receive real-time updates.
- **Export/Import**: Export projects to JSON for backups or import them easily.
- **Search**: Quickly find tasks and comments.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation
Once the server is running, visit `http://localhost:8000/docs` to see the interactive Swagger UI and try out the endpoints.
