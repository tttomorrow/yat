--  @testpoint:ts_headline函数测试（无效性测试）
--::tsquery和''顺序颠倒，报错
SELECT ts_headline('z'::tsquery,'x y z');

--高亮显示'query & similarity'字符，声明选项StartSel，StopSel,用分号分隔，合理报错
SELECT ts_headline('english',
'The most common type of search
is to find all documents containing given query terms
and return them in order of their similarity to the
query.',
to_tsquery('english', 'query & similarity'),
'StartSel = < ;StopSel = >');