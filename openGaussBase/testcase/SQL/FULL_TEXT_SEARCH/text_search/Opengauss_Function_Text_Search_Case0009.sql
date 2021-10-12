--  @testpoint:ts_headline函数测试
--不添加文本搜索配置名称（查询词是高亮显示）
SELECT ts_headline('x y z', 'z'::tsquery);
--添加文本搜索配置名称
SELECT ts_headline('english','x y z', 'z'::tsquery);
--高亮显示'query & similarity'字符，不声明选项，采用缺省值
SELECT ts_headline('english','The most common type of search is to find all documents containing given query terms and return them in order of their similarity to the
query.',to_tsquery('english', 'query & similarity'));
--高亮显示'query & similarity'字符，声明选项StartSel，StopSel
SELECT ts_headline('english','The most common type of search is to find all documents containing given query terms and return them in order of their similarity to the query.',
to_tsquery('english', 'query & similarity'),'StartSel = <, StopSel = >');

--高亮显示'query & similarity'字符，声明选项StartSel，StopSel和MaxWords，MinWords
SELECT ts_headline('english','The most common type of search is to find all documents containing given query terms and return them in order of their similarity to thequery.',
to_tsquery('english', 'query & similarity'),'StartSel = <, StopSel = >,MaxWords = 30, MinWords = 10');




