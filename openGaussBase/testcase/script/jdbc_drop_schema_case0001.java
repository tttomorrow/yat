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
import java.util.ArrayList;
import java.util.Properties;


/**
 **/
public class jdbc_drop_schema_case0001 {
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
                String sql = "drop table if exists drop_schema_case0001;";
                PreparedStatement ps_create=conn.prepareStatement(sql);
                ps_create.execute();
                sql = "create TEMPORARY table drop_schema_case0001(c0 int, c1 char(100) default ?, " +
                        "c2 varchar(5) default ?, c3 varchar2(100) default ?," +
                        "c4 nvarchar2(100) default ?, c5 clob default ?," +
                        "c6 text default ?);";
                ps_create=conn.prepareStatement(sql);
                ps_create.setString(1, "assa;--select * from pg_user;");
                ps_create.setString(2, "FALSE");
                ps_create.setString(3, "d's你好'd你好asd");
                ps_create.setString(4, "你好sdsd");
                ps_create.setString(5, "s%s/'adas");
                ps_create.setString(6, "sad''你好'sada");
                ps_create.execute();

                sql = "insert into drop_schema_case0001 values(2);";
                ps_create=conn.prepareStatement(sql);
                ps_create.execute();

                sql = "drop table if exists drop_schema_case0001;";
                ps_create=conn.prepareStatement(sql);
                ps_create.execute();

                sql = "select * from pg_tables where tablename='drop_schema_case0001';";
                ps_create = conn.prepareStatement(sql);
                ResultSet rs = ps_create.executeQuery();
                System.out.println("临时表已删除" + rs.getRow() + ".");
                ps_create.close();

            }catch (SQLException s){
                s.printStackTrace();
            }
        }
        try{
            conn.close();
        }catch (SQLException s){
            s.printStackTrace();
        }
        
    }
}