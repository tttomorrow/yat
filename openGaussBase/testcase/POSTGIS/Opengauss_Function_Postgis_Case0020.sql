-- @testpoint: PostGIS功能覆盖,计算geogA的周长,ST_Perimeter;

--step1:创建表   expect:成功
drop table if exists t_postgis_0020_01;
drop table if exists t_postgis_0020_02;
drop table if exists t_postgis_0020_03;

create table t_postgis_0020_01(smgeometry1 geometry(MultiPolygon,4490),
                          smgeometry2 geometry(MultiLineString,4490),
                          smgeometry3 geometry(MultiPoint,4490));
create table t_postgis_0020_02(smgeometry1 geometry(Polygon,4490),
                          smgeometry2 geometry(LineString,4490),
                          smgeometry3 geometry(Point,4490));
create table t_postgis_0020_03(perimeter double precision);

--step2:插入数据   expect:成功
insert into t_postgis_0020_01 values(
ST_GeomFromText('MULTIPOLYGON (((2 0, 3 1, 2 2, 1.5 1.5, 2 1, 1.5 0.5, 2 0)), ((1 0, 1.5 0.5, 1 1, 1.5 1.5, 1 2, 0 1, 1 0)))',4490),
ST_GeomFromText('MULTILINESTRING((0 0,1 1,1 2),(2 3,3 2,5 4))',4490),
ST_GeomFromText('MULTIPOINT((0 0),(1 2))',4490));
insert into t_postgis_0020_02 values(
ST_GeomFromText('POLYGON((0 0,4 0,4 4,0 4,0 0))',4490),
ST_GeomFromText('LINESTRING(0 0,1 1,1 2)',4490),
ST_GeomFromText('POINT(5 9)',4490));

--step3:结合表中数据查看   expect:成功
--计算多点smgeometry3的周长，返回值为0
select ST_Perimeter(smgeometry3) from t_postgis_0020_01;

--计算多线smgeometry2的周长，返回值为0
select ST_Perimeter(smgeometry2) from t_postgis_0020_01;

--计算多面smgeometry1的周长，返回值为所有面的和
select ST_Perimeter(smgeometry1) from t_postgis_0020_01;

--计算点smgeometry3的周长，返回值为0
select ST_Perimeter(smgeometry3) from t_postgis_0020_02;

--计算线smgeometry2的周长，返回值为0
select ST_Perimeter(smgeometry2) from t_postgis_0020_02;

--计算面smgeometry1的周长
select ST_Perimeter(smgeometry1) from t_postgis_0020_02;

--将查出来的周长值插入到指定表格的字段中
create or replace procedure p_postgis_0020()
as
sqlstat varchar(200);
begin
    for s1 in select smgeometry1 from t_postgis_0020_01 loop
    sqlstat := 'insert into t_postgis_0020_03(perimeter) values('''||ST_Perimeter(s1.smgeometry1)||''')';
    execute immediate sqlstat;
    end loop;
    for s2 in select smgeometry1 from t_postgis_0020_02 loop
    sqlstat := 'insert into t_postgis_0020_03(perimeter) values('''||ST_Perimeter(s2.smgeometry1)||''')';
    execute immediate sqlstat;
    end loop;
end;
/

call p_postgis_0020();
select perimeter from t_postgis_0020_03;

--step4:清理环境   expect:成功
drop table t_postgis_0020_01 cascade;
drop table t_postgis_0020_02 cascade;
drop procedure p_postgis_0020;
