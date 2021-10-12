--  @testpoint:文本搜索类型(tsvector类型测试)
--tsvector会自动去掉分词中重复的词条，按照一定的顺序录入（按空格分隔）
SELECT 'a fat cat sat on a mat and ate a fat rat'::tsvector;
--词条中包含空格或标点符号，可以用引号标记（其中$$是为了防止和字串中的''区分）
SELECT $$the lexeme '    ' contains spaces$$::tsvector;
--词条中包含大小写字串（先按大写排序）
SELECT $$the lexeme 'Joe''s' contains a quote$$::tsvector;
--两个字串中已经有空格（视为两个字串）
SELECT $$the lexeme 'Joe' 's' contains a quote$$::tsvector;
--词条中包含位置常量
SELECT 'a:1 fat:2 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
--词条中包含相同词重复位（相同词的重复位会被忽略掉）
SELECT 'a:6 fat:2 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
--词条中的常量为最大值16383
SELECT 'a:6 fat:16383 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
--词条中的常量设为16384（还是取默认最大值16383）
SELECT 'a:6 fat:16384 cat:3 sat:4 on:5 a:6 mat:7 and:8 ate:9 a:10 fat:11 rat:12'::tsvector;
--位置词汇用一个权来标记（默认是D，因此输出中不会出现）
SELECT 'a:1A fat:2B,4C cat:5D'::tsvector;
--位置词汇用权D表示（输出没有D）
SELECT 'fat:2D,4D cat:5D'::tsvector;
--字串中含有大写以及单词结尾包含s（原样输出）
SELECT 'The Fat Rats'::tsvector;
--字串中含有大写以及单词结尾包含es（原样输出）
SELECT 'tomatoes Fat Rats'::tsvector;
--字串中含有特殊字符，原样输出
SELECT 'Fat%*^%#Rats'::tsvector;