pluginManagement {
    repositories {
        maven {
            url = uri("https://plugins.gradle.org/m2")
            name = "Huawei Maven Mirror"
            isAllowInsecureProtocol = true
        }
        mavenCentral()
    }
}

rootProject.name = "yat"
include("yat:framework")
include("yat:sql-parser")
include("yat:schedule-parser")
include("yat:compatible")
include("yat:common")
include("yat:report")
include("yat:diff")
include("yat:access")
include("yat:setting")
include("yat:vfs")
include("yat:case-properties-parser")

