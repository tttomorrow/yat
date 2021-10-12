plugins {
    kotlin("jvm")
}


dependencies {
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")
    implementation(project(":yat:common"))
    implementation("com.fasterxml.jackson.core:jackson-databind:2.12.5")
}

tasks {
    jar {
        archiveBaseName.set("yat-${project.name}")
    }
}

