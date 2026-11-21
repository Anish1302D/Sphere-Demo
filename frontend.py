# this is the code written by madhura

from http.server import BaseHTTPRequestHandler, HTTPServer


PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f6f7fb">
  <title>Orbit — Team task board</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #202334;
      --muted: #8b8fa3;
      --line: #eceef4;
      --purple: #7658e8;
      --purple-soft: #f0edff;
      --sidebar: #202132;
      --panel: #fff;
      --canvas: #f7f8fb;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      color: var(--ink);
      background: var(--canvas);
      font: 14px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    button, input, select, textarea { font: inherit; }
    button { cursor: pointer; }
    .app { display: flex; min-height: 100vh; }
    .sidebar {
      width: 238px;
      flex: 0 0 238px;
      padding: 27px 16px 20px;
      color: #b6b7c8;
      background: var(--sidebar);
      display: flex;
      flex-direction: column;
    }
    .brand { display: flex; align-items: center; gap: 11px; padding: 0 10px 34px; color: #fff; font-size: 19px; font-weight: 750; letter-spacing: -.5px; }
    .brand-mark { width: 30px; height: 30px; border-radius: 10px; display: grid; place-items: center; background: #8064ed; color: #fff; font-size: 17px; }
    .workspace { color: #88899c; font-size: 10px; font-weight: 750; letter-spacing: 1.15px; padding: 0 11px 11px; text-transform: uppercase; }
    .nav { display: grid; gap: 5px; }
    .nav-item { width: 100%; padding: 10px 11px; color: #aeb0c1; background: transparent; border: 0; border-radius: 8px; text-align: left; display: flex; gap: 11px; align-items: center; }
    .nav-item:hover { color: white; background: #2a2b3d; }
    .nav-item.active { color: #fff; background: #343148; }
    .nav-icon { width: 18px; text-align: center; font-size: 16px; }
    .nav-count { margin-left: auto; font-size: 11px; color: #9293a7; }
    .sidebar-spacer { height: 30px; }
    .projects-heading { display: flex; align-items: center; justify-content: space-between; padding-right: 10px; }
    .add-project { border: 0; background: none; color: #aeb0c1; font-size: 18px; }
    .project { padding: 8px 11px; display: flex; gap: 10px; align-items: center; color: #aeb0c1; }
    .project-dot { width: 8px; height: 8px; border-radius: 50%; background: #e6a759; }
    .project:nth-child(3) .project-dot { background: #6bc6a5; }
    .project:nth-child(4) .project-dot { background: #7e9be8; }
    .sidebar-bottom { margin-top: auto; padding: 14px 6px 0; border-top: 1px solid #343546; display: flex; align-items: center; gap: 10px; }
    .avatar { width: 31px; height: 31px; display: inline-grid; place-items: center; flex: 0 0 auto; border-radius: 50%; color: #5740a7; background: #e6ddff; font-size: 10px; font-weight: 750; }
    .user-name { color: #f3f3f8; font-size: 12px; font-weight: 650; }
    .user-role { color: #8e90a3; font-size: 10px; }

    .main { min-width: 0; flex: 1; padding: 0 38px 36px; }
    .topbar { height: 78px; display: flex; align-items: center; justify-content: flex-end; gap: 20px; border-bottom: 1px solid var(--line); }
    .top-link { color: #74788b; font-size: 12px; }
    .top-separator { height: 20px; width: 1px; background: #e5e7ee; }
    .top-avatar { width: 32px; height: 32px; }
    .page { max-width: 1500px; margin: 0 auto; }
    .crumb { display: flex; align-items: center; gap: 8px; margin: 26px 0 11px; color: #9296a7; font-size: 12px; }
    .crumb strong { color: #64697d; font-weight: 600; }
    .title-row { display: flex; align-items: flex-start; justify-content: space-between; gap: 20px; }
    h1 { margin: 0; font-size: 27px; letter-spacing: -.8px; line-height: 1.25; }
    .subtitle { margin: 6px 0 0; color: #8b8fa1; font-size: 13px; }
    .title-actions { display: flex; align-items: center; gap: 10px; }
    .button { border: 1px solid #e6e8ef; border-radius: 8px; padding: 9px 13px; background: #fff; color: #565b6e; font-weight: 600; font-size: 12px; box-shadow: 0 1px 2px #17204408; }
    .button:hover { background: #f9f9fc; }
    .button.primary { color: #fff; background: var(--purple); border-color: var(--purple); box-shadow: 0 3px 8px #7658e82b; }
    .button.primary:hover { background: #684bd8; }
    .plus { padding-right: 5px; font-size: 16px; vertical-align: -1px; }
    .stats { margin: 25px 0 22px; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 13px; }
    .stat { min-height: 79px; padding: 15px 17px; display: flex; align-items: center; gap: 13px; background: var(--panel); border: 1px solid #edeef3; border-radius: 10px; }
    .stat-icon { width: 36px; height: 36px; display: grid; place-items: center; border-radius: 10px; background: #f0edff; color: #785de0; font-size: 16px; }
    .stat:nth-child(2) .stat-icon { background: #fff4e8; color: #e39842; }
    .stat:nth-child(3) .stat-icon { background: #e9f8f2; color: #3da77e; }
    .stat:nth-child(4) .stat-icon { background: #edf2ff; color: #6684d7; }
    .stat-number { font-size: 20px; font-weight: 750; line-height: 1.05; letter-spacing: -.4px; }
    .stat-label { margin-top: 4px; color: #8b8fa1; font-size: 11px; }
    .board-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin: 0 0 14px; }
    .toolbar-left, .toolbar-right { display: flex; align-items: center; gap: 9px; }
    .view-tabs { display: flex; gap: 4px; padding: 3px; border: 1px solid #e9eaf0; border-radius: 8px; background: #fff; }
    .view-tab { padding: 6px 11px; border: 0; border-radius: 6px; background: transparent; color: #868a9a; font-size: 11px; font-weight: 600; }
    .view-tab.active { color: #5e48bb; background: #f0edff; }
    .search { position: relative; }
    .search span { position: absolute; top: 7px; left: 10px; color: #9a9daf; font-size: 14px; }
    .search input { width: 185px; height: 34px; padding: 0 10px 0 31px; border: 1px solid #e6e8ef; border-radius: 7px; outline: none; background: white; color: var(--ink); font-size: 11px; }
    .search input:focus { border-color: #b5a7f5; box-shadow: 0 0 0 3px #7658e815; }
    .filter-select { height: 34px; padding: 0 26px 0 10px; border: 1px solid #e6e8ef; border-radius: 7px; background: #fff; color: #707588; font-size: 11px; }
    .board { display: grid; grid-template-columns: repeat(4, minmax(220px, 1fr)); align-items: start; gap: 14px; overflow-x: auto; padding-bottom: 10px; }
    .column { min-height: 320px; padding: 12px; border: 1px solid #edeef3; border-radius: 10px; background: #f1f2f7; }
    .column-head { display: flex; align-items: center; justify-content: space-between; padding: 1px 2px 12px; }
    .column-title { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 700; }
    .column-dot { width: 8px; height: 8px; border-radius: 50%; background: #a4a8ba; }
    .column[data-status="progress"] .column-dot { background: #e9a546; }
    .column[data-status="review"] .column-dot { background: #8a71e7; }
    .column[data-status="done"] .column-dot { background: #43b58a; }
    .column-count { min-width: 20px; padding: 2px 6px; border-radius: 10px; background: #e6e7ee; color: #777b8d; text-align: center; font-size: 10px; font-weight: 650; }
    .column-add { border: 0; background: transparent; color: #9094a5; font-size: 18px; line-height: 1; }
    .task-list { min-height: 260px; display: grid; align-content: start; gap: 9px; }
    .task-card { padding: 13px 13px 11px; border: 1px solid #e9eaf0; border-radius: 9px; background: #fff; box-shadow: 0 2px 4px #20233406; cursor: grab; }
    .task-card:active { cursor: grabbing; }
    .task-card.dragging { opacity: .45; }
    .task-tags { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .tag { padding: 3px 7px; border-radius: 5px; font-size: 9px; font-weight: 700; }
    .tag.design { color: #7657ce; background: #f0eaff; }
    .tag.development { color: #4285b8; background: #e8f4fc; }
    .tag.research { color: #c17a36; background: #fff2df; }
    .tag.content { color: #378e72; background: #e7f7f0; }
    .priority { color: #8c90a0; font-size: 10px; white-space: nowrap; }
    .priority.high { color: #d66b65; }
    .priority.medium { color: #d19340; }
    .task-title { margin: 11px 0 5px; font-size: 12px; font-weight: 680; line-height: 1.45; }
    .task-description { margin: 0; color: #9699a8; font-size: 10px; line-height: 1.5; }
    .task-meta { margin-top: 14px; padding-top: 10px; border-top: 1px solid #f0f1f5; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .assignee { display: flex; align-items: center; gap: 6px; min-width: 0; }
    .assignee .avatar { width: 23px; height: 23px; font-size: 8px; }
    .assignee-name { color: #777b8d; font-size: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .due { color: #999cab; font-size: 9px; white-space: nowrap; }
    .due.overdue { color: #d66b65; }
    .task-footer { display: flex; align-items: center; justify-content: space-between; margin-top: 9px; }
    .comments { color: #9a9dad; font-size: 9px; }
    .move-button { border: 0; background: none; color: #7662ca; font-size: 9px; font-weight: 650; padding: 3px 0 3px 7px; }
    .empty { color: #a0a3b0; text-align: center; font-size: 11px; padding: 22px 4px; }
    .column.drag-over { outline: 2px dashed #aa9bed; outline-offset: -4px; background: #eeebfc; }
    dialog { width: min(440px, calc(100vw - 30px)); padding: 0; border: 0; border-radius: 14px; box-shadow: 0 24px 80px #1c1c2a38; color: var(--ink); }
    dialog::backdrop { background: #20213266; backdrop-filter: blur(2px); }
    .dialog-head { padding: 20px 22px 15px; border-bottom: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; }
    .dialog-head h2 { margin: 0; font-size: 17px; }
    .close-button { border: 0; background: none; color: #85899b; font-size: 20px; }
    .form { padding: 19px 22px 22px; display: grid; gap: 13px; }
    .field { display: grid; gap: 6px; }
    .field label { color: #656a7d; font-size: 11px; font-weight: 650; }
    .field input, .field textarea, .field select { width: 100%; border: 1px solid #e4e6ed; border-radius: 7px; padding: 9px 10px; outline: none; color: var(--ink); background: #fff; font-size: 12px; }
    .field input:focus, .field textarea:focus, .field select:focus { border-color: #aa99f0; box-shadow: 0 0 0 3px #7658e815; }
    .field textarea { min-height: 68px; resize: vertical; }
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .form-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 4px; }
    @media (max-width: 1050px) {
      .main { padding-right: 22px; padding-left: 22px; }
      .board { grid-template-columns: repeat(4, minmax(215px, 1fr)); }
    }
    @media (max-width: 760px) {
      .sidebar { width: 64px; flex-basis: 64px; padding: 20px 8px; align-items: center; }
      .brand { padding: 0 0 30px; }
      .brand-name, .workspace, .nav-label, .nav-count, .sidebar-spacer, .projects-heading, .project, .sidebar-bottom .user-info { display: none; }
      .nav-item { width: 42px; height: 42px; justify-content: center; padding: 0; }
      .nav-icon { font-size: 17px; }
      .sidebar-bottom { padding: 14px 0 0; justify-content: center; }
      .main { padding: 0 16px 25px; }
      .topbar { height: 61px; }
      .top-link { display: none; }
      .title-row { align-items: flex-start; }
      h1 { font-size: 23px; }
      .title-actions .button:not(.primary) { display: none; }
      .stats { grid-template-columns: repeat(2, 1fr); gap: 9px; margin-top: 19px; }
      .stat { padding: 11px; min-height: 68px; gap: 9px; }
      .stat-icon { width: 31px; height: 31px; }
      .stat-number { font-size: 17px; }
      .board-toolbar { align-items: flex-start; flex-direction: column; }
      .toolbar-left, .toolbar-right { width: 100%; justify-content: space-between; }
      .search { flex: 1; }
      .search input { width: 100%; }
      .board { grid-template-columns: repeat(4, minmax(245px, 78vw)); }
    }
    @media (max-width: 420px) {
      .main { padding-right: 12px; padding-left: 12px; }
      .crumb { margin-top: 19px; }
      .subtitle { max-width: 220px; }
      .title-actions .primary { padding: 9px 10px; }
      .form-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div class="brand"><span class="brand-mark">◉</span><span class="brand-name">orbit</span></div>
      <div class="workspace">Workspace</div>
      <nav class="nav" aria-label="Main navigation">
        <button class="nav-item"><span class="nav-icon">⌂</span><span class="nav-label">Home</span></button>
        <button class="nav-item active"><span class="nav-icon">▦</span><span class="nav-label">My tasks</span><span class="nav-count" id="myTaskCount"></span></button>
        <button class="nav-item"><span class="nav-icon">◷</span><span class="nav-label">Inbox</span><span class="nav-count">3</span></button>
      </nav>
      <div class="sidebar-spacer"></div>
      <div class="workspace projects-heading"><span>Projects</span><button class="add-project" aria-label="Add project">+</button></div>
      <div class="project"><span class="project-dot"></span><span>Website redesign</span></div>
      <div class="project"><span class="project-dot"></span><span>Mobile app</span></div>
      <div class="project"><span class="project-dot"></span><span>Brand refresh</span></div>
      <div class="sidebar-bottom">
        <span class="avatar">JD</span>
        <div class="user-info"><div class="user-name">Jordan Davis</div><div class="user-role">Product team</div></div>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
        <span class="top-link">Help center</span><span class="top-link">⌕</span>
        <span class="top-separator"></span><span class="avatar top-avatar">JD</span>
      </header>
      <div class="page">
        <div class="crumb"><span>Projects</span><span>/</span><strong>Website redesign</strong></div>
        <section class="title-row">
          <div><h1>Website redesign</h1><p class="subtitle">Plan, track, and ship your team's best work.</p></div>
          <div class="title-actions">
            <button class="button" type="button" id="shareButton">↗ &nbsp;Share</button>
            <button class="button primary" type="button" id="openTask"><span class="plus">+</span> Add task</button>
          </div>
        </section>

        <section class="stats" aria-label="Project overview">
          <div class="stat"><span class="stat-icon">▦</span><div><div class="stat-number" id="totalStat">0</div><div class="stat-label">Total tasks</div></div></div>
          <div class="stat"><span class="stat-icon">◷</span><div><div class="stat-number" id="progressStat">0</div><div class="stat-label">In progress</div></div></div>
          <div class="stat"><span class="stat-icon">✓</span><div><div class="stat-number" id="doneStat">0</div><div class="stat-label">Completed</div></div></div>
          <div class="stat"><span class="stat-icon">♧</span><div><div class="stat-number">4</div><div class="stat-label">Team members</div></div></div>
        </section>

        <section class="board-toolbar" aria-label="Board controls">
          <div class="toolbar-left">
            <div class="view-tabs" role="group" aria-label="Task filter">
              <button class="view-tab active" data-filter="all">All tasks</button>
              <button class="view-tab" data-filter="mine">My tasks</button>
            </div>
          </div>
          <div class="toolbar-right">
            <label class="search"><span>⌕</span><input id="searchInput" type="search" placeholder="Search tasks..." aria-label="Search tasks"></label>
            <select class="filter-select" id="priorityFilter" aria-label="Filter by priority">
              <option value="all">All priorities</option><option value="high">High priority</option><option value="medium">Medium priority</option><option value="low">Low priority</option>
            </select>
          </div>
        </section>

        <section class="board" id="board" aria-label="Task board"></section>
      </div>
    </main>
  </div>

  <dialog id="taskDialog">
    <div class="dialog-head"><h2>Create a task</h2><button class="close-button" id="closeDialog" type="button" aria-label="Close">×</button></div>
    <form class="form" id="taskForm">
      <div class="field"><label for="taskTitle">Task name</label><input id="taskTitle" name="title" maxlength="90" placeholder="e.g. Design the settings page" required></div>
      <div class="field"><label for="taskDescription">Description</label><textarea id="taskDescription" name="description" maxlength="220" placeholder="Add a few details..."></textarea></div>
      <div class="form-row">
        <div class="field"><label for="taskCategory">Category</label><select id="taskCategory" name="category"><option>Design</option><option>Development</option><option>Research</option><option>Content</option></select></div>
        <div class="field"><label for="taskPriority">Priority</label><select id="taskPriority" name="priority"><option value="medium">Medium</option><option value="high">High</option><option value="low">Low</option></select></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="taskAssignee">Assignee</label><select id="taskAssignee" name="assignee"><option>Jordan Davis</option><option>Alex Morgan</option><option>Sam Rivera</option><option>Taylor Kim</option></select></div>
        <div class="field"><label for="taskDue">Due date</label><input id="taskDue" name="due" type="date"></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="taskStatus">Status</label><select id="taskStatus" name="status"><option value="todo">To do</option><option value="progress">In progress</option><option value="review">In review</option><option value="done">Done</option></select></div>
        <div></div>
      </div>
      <div class="form-actions"><button class="button" id="cancelDialog" type="button">Cancel</button><button class="button primary" type="submit">Create task</button></div>
    </form>
  </dialog>

  <script>
    const statuses = [
      { id: "todo", title: "To do" },
      { id: "progress", title: "In progress" },
      { id: "review", title: "In review" },
      { id: "done", title: "Done" }
    ];
    const seedTasks = [
      { id: "t1", title: "Finalize homepage wireframes", description: "Share the updated layout with the team for feedback.", category: "Design", priority: "high", assignee: "Alex Morgan", due: "2026-11-24", status: "todo", comments: 4 },
      { id: "t2", title: "Audit existing site content", description: "Review key pages and flag content that needs a refresh.", category: "Content", priority: "medium", assignee: "Taylor Kim", due: "2026-11-26", status: "todo", comments: 2 },
      { id: "t3", title: "Gather customer feedback", description: "Pull together the latest interview notes and themes.", category: "Research", priority: "low", assignee: "Sam Rivera", due: "2026-11-28", status: "todo", comments: 1 },
      { id: "t4", title: "Build responsive navigation", description: "Implement the new menu across desktop and mobile.", category: "Development", priority: "high", assignee: "Jordan Davis", due: "2026-11-23", status: "progress", comments: 6 },
      { id: "t5", title: "Create design system colors", description: "Document accessible color tokens for the new UI.", category: "Design", priority: "medium", assignee: "Alex Morgan", due: "2026-11-25", status: "progress", comments: 3 },
      { id: "t6", title: "Set up analytics events", description: "", category: "Development", priority: "medium", assignee: "Jordan Davis", due: "2026-11-27", status: "progress", comments: 2 },
      { id: "t7", title: "Review product page prototype", description: "Check interactions and provide final design feedback.", category: "Design", priority: "high", assignee: "Taylor Kim", due: "2026-11-22", status: "review", comments: 5 },
      { id: "t8", title: "Prepare launch announcement", description: "Draft the first version for the marketing team.", category: "Content", priority: "low", assignee: "Sam Rivera", due: "2026-11-29", status: "review", comments: 1 },
      { id: "t9", title: "Define project requirements", description: "Align on the goals and scope for the redesign.", category: "Research", priority: "medium", assignee: "Jordan Davis", due: "2026-11-18", status: "done", comments: 3 },
      { id: "t10", title: "Update brand illustration", description: "Export approved illustrations for the new pages.", category: "Design", priority: "low", assignee: "Alex Morgan", due: "2026-11-16", status: "done", comments: 2 }
    ];
    const avatarColors = ["#e6ddff", "#d9efff", "#ffe9d6", "#d8f3e8"];
    let tasks = loadTasks();
    let activeFilter = "all";
    let draggedTaskId = null;
    const board = document.getElementById("board");
    const dialog = document.getElementById("taskDialog");
    const form = document.getElementById("taskForm");

    function loadTasks() {
      try {
        const saved = localStorage.getItem("orbit-board-tasks");
        return saved ? JSON.parse(saved) : seedTasks.slice();
      } catch (error) {
        console.error("Could not load saved tasks:", error);
        return seedTasks.slice();
      }
    }

    function saveTasks() {
      try {
        localStorage.setItem("orbit-board-tasks", JSON.stringify(tasks));
      } catch (error) {
        console.error("Could not save tasks:", error);
      }
    }

    function initials(name) {
      return name.split(/\s+/).map(part => part[0]).slice(0, 2).join("").toUpperCase();
    }

    function visibleTasks() {
      const query = document.getElementById("searchInput").value.trim().toLowerCase();
      const priority = document.getElementById("priorityFilter").value;
      return tasks.filter(task => {
        const matchesQuery = !query || (task.title + " " + task.description + " " + task.assignee).toLowerCase().includes(query);
        const matchesPriority = priority === "all" || task.priority === priority;
        const matchesAssignee = activeFilter !== "mine" || task.assignee === "Jordan Davis";
        return matchesQuery && matchesPriority && matchesAssignee;
      });
    }

    function makeTaskCard(task) {
      const card = document.createElement("article");
      card.className = "task-card";
      card.draggable = true;
      card.dataset.id = task.id;

      const tags = document.createElement("div");
      tags.className = "task-tags";
      const category = document.createElement("span");
      category.className = "tag " + task.category.toLowerCase();
      category.textContent = task.category;
      const priority = document.createElement("span");
      priority.className = "priority " + task.priority;
      priority.textContent = (task.priority === "high" ? "↑ " : task.priority === "low" ? "↓ " : "• ") + task.priority[0].toUpperCase() + task.priority.slice(1);
      tags.append(category, priority);

      const title = document.createElement("h3");
      title.className = "task-title";
      title.textContent = task.title;
      card.append(tags, title);
      if (task.description) {
        const description = document.createElement("p");
        description.className = "task-description";
        description.textContent = task.description;
        card.append(description);
      }

      const meta = document.createElement("div");
      meta.className = "task-meta";
      const assignee = document.createElement("div");
      assignee.className = "assignee";
      const avatar = document.createElement("span");
      avatar.className = "avatar";
      avatar.textContent = initials(task.assignee);
      avatar.style.backgroundColor = avatarColors[task.assignee.length % avatarColors.length];
      const name = document.createElement("span");
      name.className = "assignee-name";
      name.textContent = task.assignee;
      assignee.append(avatar, name);

      const due = document.createElement("span");
      due.className = "due";
      const date = new Date(task.due + "T00:00:00");
      due.textContent = "◷ " + date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
      if (task.status !== "done" && date < new Date(new Date().toDateString())) due.classList.add("overdue");
      meta.append(assignee, due);
      card.append(meta);

      const footer = document.createElement("div");
      footer.className = "task-footer";
      const comments = document.createElement("span");
      comments.className = "comments";
      comments.textContent = "▱ " + (task.comments || 0) + " comments";
      footer.append(comments);
      if (task.status !== "done") {
        const move = document.createElement("button");
        move.className = "move-button";
        move.type = "button";
        move.textContent = task.status === "todo" ? "Start task →" : task.status === "progress" ? "Send to review →" : "Mark complete →";
        move.setAttribute("aria-label", move.textContent + ": " + task.title);
        move.addEventListener("click", () => {
          task.status = task.status === "todo" ? "progress" : task.status === "progress" ? "review" : "done";
          saveTasks();
          render();
        });
        footer.append(move);
      }
      card.append(footer);
      card.addEventListener("dragstart", event => {
        draggedTaskId = task.id;
        card.classList.add("dragging");
        event.dataTransfer.effectAllowed = "move";
        event.dataTransfer.setData("text/plain", task.id);
      });
      card.addEventListener("dragend", () => {
        draggedTaskId = null;
        card.classList.remove("dragging");
        document.querySelectorAll(".column.drag-over").forEach(column => column.classList.remove("drag-over"));
      });
      return card;
    }

    function render() {
      const filtered = visibleTasks();
      board.replaceChildren();
      statuses.forEach(status => {
        const column = document.createElement("section");
        column.className = "column";
        column.dataset.status = status.id;
        const matching = filtered.filter(task => task.status === status.id);
        const header = document.createElement("div");
        header.className = "column-head";
        const title = document.createElement("div");
        title.className = "column-title";
        const dot = document.createElement("span");
        dot.className = "column-dot";
        const label = document.createElement("span");
        label.textContent = status.title;
        const count = document.createElement("span");
        count.className = "column-count";
        count.textContent = matching.length;
        title.append(dot, label, count);
        const add = document.createElement("button");
        add.className = "column-add";
        add.type = "button";
        add.setAttribute("aria-label", "Add task to " + status.title);
        add.textContent = "+";
        add.addEventListener("click", () => {
          document.getElementById("taskStatus").value = status.id;
          dialog.showModal();
          document.getElementById("taskTitle").focus();
        });
        header.append(title, add);

        const list = document.createElement("div");
        list.className = "task-list";
        if (!matching.length) {
          const empty = document.createElement("div");
          empty.className = "empty";
          empty.textContent = "No tasks here yet";
          list.append(empty);
        } else {
          matching.forEach(task => list.append(makeTaskCard(task)));
        }
        column.append(header, list);
        column.addEventListener("dragover", event => {
          event.preventDefault();
          column.classList.add("drag-over");
        });
        column.addEventListener("dragleave", event => {
          if (!column.contains(event.relatedTarget)) column.classList.remove("drag-over");
        });
        column.addEventListener("drop", event => {
          event.preventDefault();
          column.classList.remove("drag-over");
          const id = event.dataTransfer.getData("text/plain") || draggedTaskId;
          const task = tasks.find(item => item.id === id);
          if (task && task.status !== status.id) {
            task.status = status.id;
            saveTasks();
            render();
          }
        });
        board.append(column);
      });
      const completed = tasks.filter(task => task.status === "done").length;
      document.getElementById("totalStat").textContent = tasks.length;
      document.getElementById("progressStat").textContent = tasks.filter(task => task.status === "progress").length;
      document.getElementById("doneStat").textContent = completed;
      document.getElementById("myTaskCount").textContent = tasks.filter(task => task.assignee === "Jordan Davis" && task.status !== "done").length;
    }

    document.getElementById("openTask").addEventListener("click", () => {
      form.reset();
      document.getElementById("taskStatus").value = "todo";
      dialog.showModal();
      document.getElementById("taskTitle").focus();
    });
    document.getElementById("closeDialog").addEventListener("click", () => dialog.close());
    document.getElementById("cancelDialog").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", event => {
      if (event.target === dialog) dialog.close();
    });
    form.addEventListener("submit", event => {
      event.preventDefault();
      const data = new FormData(form);
      const due = data.get("due") || new Date().toISOString().slice(0, 10);
      tasks.unshift({
        id: "t" + Date.now(),
        title: data.get("title").trim(),
        description: data.get("description").trim(),
        category: data.get("category"),
        priority: data.get("priority"),
        assignee: data.get("assignee"),
        due,
        status: data.get("status"),
        comments: 0
      });
      saveTasks();
      render();
      dialog.close();
    });
    document.getElementById("searchInput").addEventListener("input", render);
    document.getElementById("priorityFilter").addEventListener("change", render);
    document.querySelectorAll(".view-tab").forEach(tab => tab.addEventListener("click", () => {
      activeFilter = tab.dataset.filter;
      document.querySelectorAll(".view-tab").forEach(item => item.classList.toggle("active", item === tab));
      render();
    }));
    document.getElementById("shareButton").addEventListener("click", async event => {
      const button = event.currentTarget;
      try {
        await navigator.clipboard.writeText(location.href);
        button.textContent = "✓ Copied";
      } catch (error) {
        button.textContent = "Share unavailable";
        console.error("Could not copy the board link:", error);
      }
      setTimeout(() => { button.innerHTML = "↗ &nbsp;Share"; }, 1600);
    });
    render();
  </script>
</body>
</html>"""


class BoardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        content = PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format_string, *args):
        print("%s - %s" % (self.address_string(), format_string % args))


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print("Team task board running at http://%s:%s" % address)
    HTTPServer(address, BoardHandler).serve_forever()
