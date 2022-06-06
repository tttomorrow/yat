"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.sql.*;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Properties;


/**
 **/
public class Opengauss_Function_Guc_Query_Case0039{
    static public String driver = "org.postgresql.Driver";
    public static Properties getConfigFromFile(String filePath) {
        Properties props = new Properties();
        try {
            BufferedInputStream config = new BufferedInputStream(new FileInputStream(filePath));
            props.load(config);
        } catch (Exception e) {
            e.printStackTrace();
        }
        return props;
    }

    public static String genURLFromPro(Properties props) {
        String hostname = props.getProperty("hostname");
        String[] hostnames = hostname.split(",");
        String port = props.getProperty("port");
        String[] ports = port.split(",");
        String dbname = props.getProperty("dbname");
        return genURLFromHostsPortsDBname(hostnames, ports, dbname);
    }

    public static String genURLFromHostsPortsDBname(String[] hostnames, String[] ports, String dbname) {
        String sourceURL;
        if (hostnames.length == 1) {
            sourceURL = "jdbc:postgresql://" + hostnames[0] + ":" + ports[0] + "/" + dbname;
        } else {
            ArrayList<String> ip_port_pare = new ArrayList<>();
            if (ports.length == 1) {
                for (String ip : hostnames) {
                    ip_port_pare.add(ip + ":" + ports[0]);
                }
            } else {
                for (int i = 0; i < hostnames.length; i++) {
                    ip_port_pare.add(hostnames[i] + ":" + ports[i]);
                }
            }
            sourceURL = "jdbc:postgresql://" + String.join(",", ip_port_pare) + "/" + dbname;
        }
        return sourceURL;
    }

    public static Connection GetConnection(Properties props) {
        Connection connR;
        String sourceURL = genURLFromPro(props);
        try {
            Class.forName(driver).newInstance();
            connR = DriverManager.getConnection(sourceURL, props);
        } catch (Exception var10) {
            var10.printStackTrace();
            return null;
        }
        return connR;
    }


    public static void main(String[] args) {
        Properties pros = new Properties();
        Properties pros_conf=null;
        String jdbc_config_file = null;
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--config-file":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                case "-F":
                    jdbc_config_file = args[i + 1];
                    pros_conf=getConfigFromFile(jdbc_config_file);
                    break;
                default:
                    break;
            }
        }
        //建立连接
        if (pros_conf!=null){
            //以参数为准，覆盖配置文件中的
            pros_conf.putAll(pros);
        }
        Connection conn = GetConnection(pros_conf);
        System.out.println(conn);
        if(conn==null){
            System.out.println("连接失败");
            return;
        }else{
            try{
                System.out.println("清空hash table");
                String sql = "select reset_unique_sql('GLOBAL','ALL',100)";
                PreparedStatement ps_clean1=conn.prepareStatement(sql);
                ResultSet res_clean1=ps_clean1.executeQuery();
                ResultSetMetaData metaData1 = res_clean1.getMetaData();
                int columnCount1 = metaData1.getColumnCount();
                while (res_clean1.next()) {
                    for (int i = 1; i <= columnCount1; i++) {
                        System.out.print("清空hash table" + res_clean1.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_clean1.close();

                System.out.println("查询记录条数");
                sql = "select count(va) from (select get_instr_unique_sql() as va)";
                PreparedStatement ps_clean2=conn.prepareStatement(sql);
                ResultSet res_clean2=ps_clean2.executeQuery();
                ResultSetMetaData metaData2 = res_clean2.getMetaData();
                int columnCount2 = metaData2.getColumnCount();
                while (res_clean2.next()) {
                    for (int i = 1; i <= columnCount2; i++) {
                        System.out.print("查询记录条数" + res_clean2.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_clean2.close();

                System.out.println("创建表");
                sql = "drop table if exists jdbc_unique_table cascade;" +
                    "create table jdbc_unique_table(No int, name int, sex int)";
                PreparedStatement ps_create=conn.prepareStatement(sql);
                ps_create.execute();
                ps_create.close();

                System.out.println("P阶段");
                sql = "insert into jdbc_unique_table values(?, ?, ?);";
                PreparedStatement ps_insert=conn.prepareStatement(sql);

                System.out.println("再次查询记录条数");
                sql = "select count(va) " +
                    "from (select get_instr_unique_sql() as va);";
                PreparedStatement ps_query4=conn.prepareStatement(sql);
                ResultSet res_query4=ps_query4.executeQuery();
                ResultSetMetaData metaData4 = res_query4.getMetaData();
                int columnCount4 = metaData4.getColumnCount();
                while (res_query4.next()) {
                    for (int i = 1; i <= columnCount4; i++) {
                        System.out.print("再次查询记录条数" +
                        res_query4.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_query4.close();

                System.out.println("执行大量unique_sql 触发自动淘汰");
                for (int i=0;i<16;i++){
                    sql = "drop table if exists testUniqueSql" + i +
                        ";create table testUniqueSql" + i +"(a int, b int);" +
                        "insert into testUniqueSql" + i +" values (1);" +
                        ";select a from testUniqueSql" + i +
                        ";select b from testUniqueSql" + i +
                        ";select * from testUniqueSql" + i +
                        ";drop table if exists testUniqueSql" + i +
                        ";select 1;";
                    PreparedStatement ps_sql=conn.prepareStatement(sql);
                    ps_sql.execute();
                    ps_sql.close();
                }

                System.out.println("查询触发自动淘汰后条数");
                sql = "select count(va) " +
                    "from (select get_instr_unique_sql() as va);";
                PreparedStatement ps_query5=conn.prepareStatement(sql);
                ResultSet res_query5=ps_query5.executeQuery();
                ResultSetMetaData metaData5 = res_query5.getMetaData();
                int columnCount5 = metaData5.getColumnCount();
                while (res_query5.next()) {
                    for (int i = 1; i <= columnCount5; i++) {
                        System.out.print("查询触发自动淘汰后条数"
                        + res_query5.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_query5.close();

                System.out.println("B E阶段");
                ps_insert.setObject(1, 2);
                ps_insert.setObject(2, 4);
                ps_insert.setObject(3, 6);
                try {
                    ps_insert.execute();
                } catch (Exception e) {
                    e.printStackTrace();
                }

                System.out.println("查询B/E阶段自动淘汰后记录条数");
                sql = "select count(va) from (select get_instr_unique_sql() as va)";
                PreparedStatement ps_query6=conn.prepareStatement(sql);
                ResultSet res_query6=ps_query6.executeQuery();
                ResultSetMetaData metaData6 = res_query6.getMetaData();
                int columnCount6 = metaData6.getColumnCount();
                while (res_query6.next()) {
                    for (int i = 1; i <= columnCount6; i++) {
                        System.out.print("查询B/E阶段自动淘汰后记录条数" +
                        res_query6.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_query6.close();

                System.out.println("查询插入的数据");
                sql = "select * from jdbc_unique_table";
                PreparedStatement ps_query7=conn.prepareStatement(sql);
                ResultSet res_query7=ps_query7.executeQuery();
                ResultSetMetaData metaData7 = res_query7.getMetaData();
                int columnCount7 = metaData7.getColumnCount();
                while (res_query7.next()) {
                    for (int i = 1; i <= columnCount7; i++) {
                        System.out.print("查询插入的数据" + res_query7.getString(i) + "\t");
                    }
                    System.out.println();
                }
                ps_query7.close();
                
            }catch (SQLException s){
                s.printStackTrace();
            }
        }
        try{
            System.out.println("清理环境 删除表");
            String sql = "drop table jdbc_unique_table";
            PreparedStatement ps_drop=conn.prepareStatement(sql);
            ps_drop.execute();
            ps_drop.close();
            conn.close();
        }catch (SQLException s){
            s.printStackTrace();
        }
        
    }
}