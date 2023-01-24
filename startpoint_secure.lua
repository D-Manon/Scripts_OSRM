WayHandlers = require("lib/way_handlers")

local Startpoint_secure = {}

-- determine if this way can be used as a start/end point for routing https://github.com/Project-OSRM/osrm-profiles-contrib/blob/master/5/18/does_not_starts_or_ends_in_the_midst_of_motorway_or_tunnel/lib/startpoint_secure.lua
function Startpoint_secure.startpoint_secure(profile,way,result,data)
  local highway = way:get_value_by_key("highway")
  local tunnel = way:get_value_by_key("tunnel")

  if highway ~= "motorway" and highway ~= "motorway_link" and highway ~= "airway" and (not tunnel or tunnel == "")  and not airway then
    WayHandlers.startpoint(way,result,data,profile)
  else
    result.is_startpoint = false
  end
end

return Startpoint_secure
