-- @testpoint: 函数current_setting(setting_name)，用于以查询形式获取setting_name的当前值.与show方式查看结果等效

show datestyle;
select current_setting('datestyle');
show geqo_threshold;
select current_setting('geqo_threshold');
show track_activities;
select current_setting('track_activities');

