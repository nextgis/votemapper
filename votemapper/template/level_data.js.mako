<% import json %>
levels[${ level.id }].data = ${ env.level_json(level.id)};
initializeLevel(${ level.id});