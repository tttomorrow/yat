-- @testpoint: popen函数把路径转换为开放路径,入参给闭合路径
SELECT popen(path '((0,0),(1,1),(2,0))') AS RESULT;