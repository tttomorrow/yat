-- @testpoint: popen函数将路径转换为开放路径,入参给开放路径
SELECT popen(path '[(0,0),(1,1),(2,0)]') AS RESULT;