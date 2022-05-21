-- @testpoint: PostGIS功能覆盖,计算geogA的面积,ST_Area

--step1:创建表   expect:成功
drop table if exists t_postgis_0019_01;
drop table if exists t_postgis_0019_02;

create table t_postgis_0019_01(smgeometry1 geometry(MultiPolygon,4490),
                          smgeometry2 geometry(Polygon,4490));
create table t_postgis_0019_02(area double precision);

--step2:插入数据   expect:成功
insert into t_postgis_0019_01 values(
ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490),
ST_GeomFromText('POLYGON((0 0,4 0,4 4,0 4,0 0))',4490));
insert into t_postgis_0019_01 values(
ST_GeomFromText('MULTIPOLYGON(((0 0,4 0,4 4,0 4,0 0),(1 1,2 1,2 2,1 2,1 1)), ((-1 -1,-1 -2,-2 -2,-2 -1,-1 -1)))',4490),
ST_GeomFromText('POLYGON((0 0,4 0,4 4,0 4,0 0),(1 1, 2 1, 2 2, 1 2,1 1))',4490));

--step3:结合表查看数据   expect:成功
--计算多面smgeometry1的面积
select ST_Area(smgeometry1) from t_postgis_0019_01;

--计算面smgeometry2的面积
select ST_Area(smgeometry2) from t_postgis_0019_01;

--将查出来的面积值插入到指定表格的字段中
create or replace procedure p_postgis_0019()
as
sqlstat varchar(200);
begin
    for s1 in select smgeometry1 from t_postgis_0019_01 loop
    sqlstat := 'insert into t_postgis_0019_02(area) values('''||ST_Area(s1.smgeometry1)||''')';
    execute immediate sqlstat;
    end loop;
    for s2 in select smgeometry2 from t_postgis_0019_01 loop
    sqlstat := 'insert into t_postgis_0019_02(area) values('''||ST_Area(s2.smgeometry2)||''')';
    execute immediate sqlstat;
    end loop;
end;
/

call p_postgis_0019();
select area from t_postgis_0019_02;

--step4:清理环境   expect:成功
drop table t_postgis_0019_01 cascade;
drop table t_postgis_0019_02 cascade;
drop procedure p_postgis_0019;
