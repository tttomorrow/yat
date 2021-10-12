plugins {
    java
    kotlin("jvm")
}

dependencies {
    implementation(project(":yat:setting"))
    implementation(project(":yat:common"))
    implementation(project(":yat:schedule-parser"))
    implementation("com.fasterxml.jackson.core:jackson-databind:2.12.5")
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")

    compileOnly("org.projectlombok:lombok:1.18.6")
    annotationProcessor("org.projectlombok:lombok:1.18.6")

    testImplementation("org.junit.jupiter:junit-jupiter-api:5.8.0")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine:5.8.0")

}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}
