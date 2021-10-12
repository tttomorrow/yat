--  @testpoint:文本搜索类型（tsquery）
--检索的词汇使用&连接（布尔操作符也会原样输出）
SELECT 'fat & rat'::tsquery;
--检索的词汇使用&和！连接（布尔操作符也会原样输出）
SELECT 'fat & rat & ! cat'::tsquery;
--检索的词汇使用&和！以及|连接（布尔操作符也会原样输出）
SELECT 'fat & rat & ! cat | dog'::tsquery;
--检索词汇加括号
SELECT 'fat & (rat | cat)'::tsquery;
--检索词汇用权表示（权用小写表示，输出为大写）
SELECT 'fat:ab & cat'::tsquery;
--检索词汇用权表示（权用大写表示，输出为大写）
SELECT 'fat:AB & cat'::tsquery;
--检索词汇用权D表示（输出有D）
SELECT 'fat:AB & catD'::tsquery;
--检索词汇用多个权表示
SELECT 'fat:ABCD & catD'::tsquery;
--检索词汇的权大小写混合（输出为全大写）
SELECT 'fat:abCD & catD'::tsquery;
--指定前缀匹配（匹配tsvector中以super开头的任意单词）
SELECT 'super:*'::tsquery;