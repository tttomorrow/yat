-- @testpoint: set session命令设置配置参数allocate_mem_cost值超范围，合理报错（user类型）
--set session to 命令设置配置参数
set session allocate_mem_cost to 1E+309;
set session allocate_mem_cost to -1;
--set session =命令设置配置参数
set session allocate_mem_cost = -1E+308;
set session allocate_mem_cost = -1;