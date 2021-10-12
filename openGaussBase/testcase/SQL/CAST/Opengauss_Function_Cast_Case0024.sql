-- @testpoint: unknown和已知类型的参数，并且所有已知类型的参数有相同的类型

-- @testpoint：unknown和已知类型的参数，并且所有已知类型的参数有相同的类型：success
-- @regexp_like(text,text,text)
explain performance select regexp_like('test0024','test','c');
explain performance select regexp_like(123,'[12]','c');

--清理环境
--no need to clean