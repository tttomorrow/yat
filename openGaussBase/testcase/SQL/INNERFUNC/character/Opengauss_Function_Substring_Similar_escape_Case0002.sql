-- @testpoint:  函数similar_escape(pat text, esc text)，将一个 SQL:2008风格的正则表达式转换为POSIX风格。参数为无效值时，合理报错

--当Escape参数为两个字符时，合理报错
select similar_escape('/<.*>/','12');
select similar_escape('?.*','12');