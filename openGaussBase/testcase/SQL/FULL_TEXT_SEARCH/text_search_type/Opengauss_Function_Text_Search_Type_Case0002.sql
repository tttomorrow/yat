--  @testpoint:文本搜索类型(tsvector类型无效值测试)
--位置常量和权混合使用，合理报错
SELECT 'fat:2AB, cat:5D'::tsvector;
--字串中含有中文，合理报错
SELECT '检索' 'Fat Rats'::tsvector;
--位置词汇用权E表示，合理报错
SELECT 'a:1E fat:2B,4C cat:5D'::tsvector;
