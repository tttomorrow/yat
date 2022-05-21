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
import java.time.OffsetDateTime;
import java.util.ArrayList;
import java.util.Properties;


/**
 **/
public class jdbc_set_get_object_case0022 {
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
        if(conn==null){
            System.out.println("连接失败");
            return;
        }else{
            try{
                String sql = "select * from jdbc_set_get_object_case0022_date ;";
                PreparedStatement ps_select=conn.prepareStatement(sql);
                ResultSet rs=ps_select.executeQuery();
                rs.next();
                LocalDate result1 = rs.getObject(1, LocalDate.class);
                System.out.println("LocalDate结果：" + result1) ;
                ps_select.close();

                sql = "select * from jdbc_set_get_object_case0022_stamptz ;";
                ps_select=conn.prepareStatement(sql);
                rs = ps_select.executeQuery();
                rs.next();
                OffsetDateTime result = rs.getObject(1, OffsetDateTime.class);
                System.out.println("OffsetDateTime结果：" + result) ;
                ps_select.close();

                sql = "select * from jdbc_set_get_object_case0022_stamp ;";
                ps_select=conn.prepareStatement(sql);
                rs = ps_select.executeQuery();
                rs.next();
                LocalDateTime result2 = rs.getObject(1, LocalDateTime.class);
                System.out.println("LocalDateTime结果：" + result2) ;
                ps_select.close();

                sql = "select * from jdbc_set_get_object_case0022_time ;";
                ps_select=conn.prepareStatement(sql);
                rs = ps_select.executeQuery();
                rs.next();
                LocalTime result3 = rs.getObject(1, LocalTime.class);
                System.out.println("LocalTime结果：" + result3) ;
                ps_select.close();
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