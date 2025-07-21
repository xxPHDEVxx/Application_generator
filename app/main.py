from generator.generator import Generator

if __name__ == "__main__":
    informations = """Description du poste
We are seeking a skilled and experienced Data Engineer. This position requires fluency in either French or Dutch, along with proficiency in English, and a strong background in data engineering best practices.

Key responsibilities

Design, build, and maintain robust, scalable, and efficient data pipelines using Azure Data Services (e.g., Azure Data Factory, Azure Synapse, Azure Databricks, Azure SQL, etc.)

Develop and manage ETL/ELT processes to ingest, transform, and store data from various sources

Collaborate with data scientists, analysts, and business stakeholders to understand data needs and translate them into technical solutions

Ensure data quality, security, and governance are enforced across data workflows

Monitor, troubleshoot, and optimize existing pipelines and data systems for performance and cost-efficiency

Participate in the design of data models, data lakes, and warehouses to support analytics and reporting

Work in an Agile environment and actively contribute to sprint planning, stand-ups, and code reviews

Required qualifications

5+ years of experience in data engineering roles

Proven expertise with Microsoft Azure data services

Proficiency in SQL, Python or Scala, and cloud-based ETL tools

Hands-on experience with tools like Azure Data Factory, Azure Databricks, Azure Synapse Analytics, and Azure Storage

Strong knowledge of data modeling, data warehousing, and data architecture

Understanding of CI/CD practices and Version Control tools (e.g., GIT)

Fluency in English and either French or Dutch

Nice to have

Experience with DevOps or infrastructure as code (e.g., TerraForm, ARM templates)

Knowledge of data governance frameworks (e.g., Microsoft Purview)

Familiarity with Power BI or other reporting tools

Experience working in regulated or high-compliance industries"""

    generator = Generator(informations)
    print(generator.run())