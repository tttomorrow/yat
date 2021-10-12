--  @testpoint:set session 命令和set local命令设置配置参数allocate_mem_cost（user类型）
--查看参数allocate_mem_cost，默认为0
show allocate_mem_cost;
--set session to命令设置参数allocate_mem_cost为DBL_MAX最大值
set session allocate_mem_cost to 1E+308;
--查看参数allocate_mem_cost值
show allocate_mem_cost;
--恢复默认值
reset allocate_mem_cost;
--查看参数allocate_mem_cost值恢复默认值0
show allocate_mem_cost;

--set session =命令设置参数allocate_mem_cost为DBL_MAX最大值
set session allocate_mem_cost = 1E+308;
--查看参数allocate_mem_cost值
show allocate_mem_cost;
--恢复默认值为0
reset allocate_mem_cost;

--set local命令设置allocate_mem_cost参数，
set local allocate_mem_cost = 1E+308;
--查看参数allocate_mem_cost值，set local命令不生效，依然是默认值0
show allocate_mem_cost;