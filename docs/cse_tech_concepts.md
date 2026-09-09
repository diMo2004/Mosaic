# CSE Technology & Concept Knowledge Graph

## Purpose

This document maps major **Computer Science and Engineering (CSE)** concepts, technologies, tools, frameworks, languages, architectures, and applications as a connected knowledge graph.

**Edge semantics used in the graphs:**

- `parent` — the node is a subfield/subconcept of another node.
- `related` — concepts are strongly associated.
- `implements` — a technology implements a concept/pattern.
- `used-by` — a technology is commonly used by another technology/domain.
- `builds-on` — one concept is foundational to another.
- `alternative` — commonly comparable or interchangeable technologies.

---

# 1. Master CSE Knowledge Graph

```mermaid
graph TD
    CSE[CSE / Computer Science & Engineering]

    CSE --> CS[Computer Science]
    CSE --> CE[Computer Engineering]
    CSE --> SE[Software Engineering]
    CSE --> AI[Artificial Intelligence]
    CSE --> DS[Data Science]
    CSE --> Cyber[Cybersecurity]
    CSE --> Networks[Computer Networks]
    CSE --> Systems[Computer Systems]
    CSE --> Web[Web Technologies]
    CSE --> Mobile[Mobile Computing]
    CSE --> Cloud[Cloud Computing]
    CSE --> DevOps[DevOps / Platform Engineering]
    CSE --> DB[Databases]
    CSE --> Graphics[Computer Graphics]
    CSE --> HCI[Human Computer Interaction]
    CSE --> Theory[Theory of Computation]
    CSE --> Embedded[Embedded Systems]
    CSE --> Blockchain[Blockchain / Distributed Ledger]
    CSE --> IoT[Internet of Things]

    CS --> DSA[Data Structures & Algorithms]
    CS --> OS[Operating Systems]
    CS --> PL[Programming Languages]
    CS --> Compilers[Compiler Design]
    CS --> Architecture[Computer Architecture]
    CS --> Distributed[Distributed Systems]

    AI --> ML[Machine Learning]
    AI --> DL[Deep Learning]
    AI --> NLP[Natural Language Processing]
    AI --> CV[Computer Vision]
    AI --> GenAI[Generative AI]
    AI --> Agents[AI Agents]
    DS --> Statistics[Statistics]
    DS --> DataEngineering[Data Engineering]
    DS --> Visualization[Data Visualization]

    Web --> Frontend[Frontend]
    Web --> Backend[Backend]
    Web --> APIs[APIs]
    Web --> FullStack[Full Stack]

    Cloud --> Compute[Compute]
    Cloud --> Storage[Cloud Storage]
    Cloud --> Serverless[Serverless]
    Cloud --> Containers[Containers]
    Cloud --> Orchestration[Orchestration]

    Cyber --> AppSec[Application Security]
    Cyber --> NetworkSec[Network Security]
    Cyber --> Cryptography[Cryptography]
    Cyber --> Identity[Identity & Access Management]
```

---

# 2. Programming Languages & Paradigms

```mermaid
graph TD
    PL[Programming Languages]

    PL --> Imperative[Imperative]
    PL --> OOP[Object Oriented]
    PL --> Functional[Functional]
    PL --> Declarative[Declarative]
    PL --> Concurrent[Concurrent / Parallel]
    PL --> Scripting[Scripting]
    PL --> Systems[Systems Programming]

    Imperative --> C[C]
    Systems --> CPP[C++]
    Systems --> Rust[Rust]
    Systems --> Zig[Zig]

    OOP --> Java[Java]
    OOP --> CSharp[C#]
    OOP --> CPP
    OOP --> Python[Python]

    Functional --> Haskell[Haskell]
    Functional --> Scala[Scala]
    Functional --> Elixir[Elixir]
    Functional --> Clojure[Clojure]

    Scripting --> Python
    Scripting --> JS[JavaScript]
    Scripting --> Bash[Bash]
    Scripting --> PHP[PHP]
    Scripting --> Ruby[Ruby]

    Declarative --> SQL[SQL]
    Declarative --> HTML[HTML]
    Declarative --> CSS[CSS]

    JS --> TS[TypeScript]
    Java --> Kotlin[Kotlin]
    Java --> Android[Android]
    Swift[Swift] --> iOS[iOS]

    PL --> Memory[Memory Management]
    PL --> Types[Type Systems]
    PL --> Generics[Generics]
    PL --> Concurrency[Concurrency]
    PL --> Exceptions[Exception Handling]
    PL --> Testing[Testing]
```

---

# 3. Data Structures & Algorithms

```mermaid
graph TD
    DSA[Data Structures & Algorithms]

    DSA --> Linear[Linear Structures]
    DSA --> NonLinear[Non-Linear Structures]
    DSA --> Hashing[Hashing]
    DSA --> Sorting[Sorting]
    DSA --> Searching[Searching]
    DSA --> Graphs[Graph Algorithms]
    DSA --> DP[Dynamic Programming]
    DSA --> Greedy[Greedy Algorithms]
    DSA --> Divide[Divide & Conquer]
    DSA --> Complexity[Complexity Analysis]

    Linear --> Array[Array]
    Linear --> LinkedList[Linked List]
    Linear --> Stack[Stack]
    Linear --> Queue[Queue]
    Linear --> Deque[Deque]

    NonLinear --> Tree[Tree]
    NonLinear --> Heap[Heap]
    NonLinear --> Trie[Trie]
    NonLinear --> Graph[Graph]

    Tree --> BST[Binary Search Tree]
    Tree --> AVL[AVL Tree]
    Tree --> Segment[Segment Tree]
    Tree --> BTree[B-Tree]

    Heap --> PriorityQueue[Priority Queue]

    Sorting --> QuickSort[Quick Sort]
    Sorting --> MergeSort[Merge Sort]
    Sorting --> HeapSort[Heap Sort]
    Sorting --> CountingSort[Counting Sort]

    Searching --> BinarySearch[Binary Search]
    Searching --> BFS[Breadth First Search]
    Searching --> DFS[Depth First Search]

    Graphs --> BFS
    Graphs --> DFS
    Graphs --> Dijkstra[Dijkstra]
    Graphs --> Bellman[Bellman-Ford]
    Graphs --> Floyd[Floyd-Warshall]
    Graphs --> MST[Minimum Spanning Tree]

    Complexity --> BigO[Big-O]
    Complexity --> BigOmega[Big-Omega]
    Complexity --> BigTheta[Big-Theta]
```

---

# 4. Operating Systems & Computer Architecture

```mermaid
graph TD
    Systems[Computer Systems]

    Systems --> Architecture[Computer Architecture]
    Systems --> OS[Operating Systems]

    Architecture --> CPU[CPU]
    Architecture --> GPU[GPU]
    Architecture --> ISA[Instruction Set Architecture]
    Architecture --> MemoryHierarchy[Memory Hierarchy]
    Architecture --> Cache[CPU Cache]
    Architecture --> RAM[RAM]
    Architecture --> Storage[Storage]

    CPU --> ALU[ALU]
    CPU --> ControlUnit[Control Unit]
    CPU --> Registers[Registers]
    CPU --> Pipeline[Instruction Pipeline]
    CPU --> Multicore[Multicore Processing]

    OS --> Kernel[Kernel]
    OS --> Processes[Processes]
    OS --> Threads[Threads]
    OS --> Scheduling[CPU Scheduling]
    OS --> MemoryManagement[Memory Management]
    OS --> VirtualMemory[Virtual Memory]
    OS --> FileSystems[File Systems]
    OS --> IPC[Interprocess Communication]
    OS --> Drivers[Device Drivers]
    OS --> Security[OS Security]

    Processes --> Threads
    Threads --> Synchronization[Synchronization]
    Synchronization --> Mutex[Mutex]
    Synchronization --> Semaphore[Semaphore]
    Synchronization --> Deadlock[Deadlock]

    OS --> Linux[Linux]
    OS --> Windows[Windows]
    OS --> Unix[Unix]
    OS --> MacOS[macOS]
```

---

# 5. Databases & Data Management

```mermaid
graph TD
    DB[Databases]

    DB --> Relational[Relational Databases]
    DB --> NoSQL[NoSQL]
    DB --> NewSQL[NewSQL]
    DB --> OLAP[OLAP]
    DB --> OLTP[OLTP]
    DB --> DistributedDB[Distributed Databases]
    DB --> DataWarehouse[Data Warehousing]
    DB --> DataLake[Data Lakes]

    Relational --> PostgreSQL[PostgreSQL]
    Relational --> MySQL[MySQL]
    Relational --> SQLite[SQLite]
    Relational --> Oracle[Oracle Database]
    Relational --> SQLServer[SQL Server]

    NoSQL --> Document[Document DB]
    NoSQL --> KeyValue[Key Value DB]
    NoSQL --> GraphDB[Graph DB]
    NoSQL --> WideColumn[Wide Column DB]

    Document --> MongoDB[MongoDB]
    KeyValue --> Redis[Redis]
    GraphDB --> Neo4j[Neo4j]
    WideColumn --> Cassandra[Cassandra]

    DB --> SQL[SQL]
    SQL --> Joins[Joins]
    SQL --> Indexing[Indexing]
    SQL --> Transactions[Transactions]
    Transactions --> ACID[ACID]
    ACID --> Atomicity[Atomicity]
    ACID --> Consistency[Consistency]
    ACID --> Isolation[Isolation]
    ACID --> Durability[Durability]

    DistributedDB --> CAP[CAP Theorem]
    DistributedDB --> Replication[Replication]
    DistributedDB --> Sharding[Sharding]
```

---

# 6. Software Engineering & Development

```mermaid
graph TD
    SE[Software Engineering]

    SE --> SDLC[SDLC]
    SE --> Requirements[Requirements Engineering]
    SE --> Architecture[Software Architecture]
    SE --> DesignPatterns[Design Patterns]
    SE --> Testing[Software Testing]
    SE --> VersionControl[Version Control]
    SE --> CodeQuality[Code Quality]
    SE --> Agile[Agile]
    SE --> ProjectManagement[Project Management]

    VersionControl --> Git[Git]
    Git --> GitHub[GitHub]
    Git --> GitLab[GitLab]
    Git --> Bitbucket[Bitbucket]

    Testing --> Unit[Unit Testing]
    Testing --> Integration[Integration Testing]
    Testing --> System[System Testing]
    Testing --> E2E[End-to-End Testing]
    Testing --> Performance[Performance Testing]
    Testing --> SecurityTesting[Security Testing]

    DesignPatterns --> Singleton[Singleton]
    DesignPatterns --> Factory[Factory]
    DesignPatterns --> Observer[Observer]
    DesignPatterns --> Strategy[Strategy]
    DesignPatterns --> Adapter[Adapter]

    Architecture --> Monolith[Monolith]
    Architecture --> Microservices[Microservices]
    Architecture --> EventDriven[Event Driven]
    Architecture --> Layered[Layered Architecture]
    Architecture --> Hexagonal[Hexagonal Architecture]
```

---

# 7. Web Development

```mermaid
graph TD
    Web[Web Development]

    Web --> Frontend[Frontend]
    Web --> Backend[Backend]
    Web --> FullStack[Full Stack]
    Web --> API[API]
    Web --> Protocols[Web Protocols]

    Frontend --> HTML[HTML]
    Frontend --> CSS[CSS]
    Frontend --> JavaScript[JavaScript]
    Frontend --> TypeScript[TypeScript]

    JavaScript --> React[React]
    JavaScript --> Vue[Vue]
    JavaScript --> Angular[Angular]
    JavaScript --> NextJS[Next.js]
    TypeScript --> NextJS

    CSS --> Tailwind[Tailwind CSS]
    CSS --> Bootstrap[Bootstrap]

    Backend --> Node[Node.js]
    Backend --> Django[Django]
    Backend --> FastAPI[FastAPI]
    Backend --> Spring[Spring Boot]
    Backend --> Express[Express.js]
    Backend --> Laravel[Laravel]

    API --> REST[REST]
    API --> GraphQL[GraphQL]
    API --> GRPC[gRPC]
    API --> WebSockets[WebSockets]

    Protocols --> HTTP[HTTP]
    Protocols --> HTTPS[HTTPS]
    Protocols --> DNS[DNS]
    Protocols --> TLS[TLS]

    FullStack --> MERN[MERN]
    FullStack --> MEAN[MEAN]
    FullStack --> DjangoReact[Django + React]
```

---

# 8. Computer Networks

```mermaid
graph TD
    Networks[Computer Networks]

    Networks --> OSI[OSI Model]
    Networks --> TCPIP[TCP/IP]
    Networks --> LAN[LAN]
    Networks --> WAN[WAN]
    Networks --> Routing[Routing]
    Networks --> Switching[Switching]
    Networks --> Wireless[Wireless]

    OSI --> Physical[Physical Layer]
    OSI --> DataLink[Data Link Layer]
    OSI --> Network[Network Layer]
    OSI --> Transport[Transport Layer]
    OSI --> Session[Session Layer]
    OSI --> Presentation[Presentation Layer]
    OSI --> Application[Application Layer]

    TCPIP --> TCP[TCP]
    TCPIP --> UDP[UDP]
    TCPIP --> IP[IP]
    TCPIP --> HTTP
    TCPIP --> DNS

    Routing --> BGP[BGP]
    Routing --> OSPF[OSPF]
    Routing --> RIP[RIP]

    Network --> IPv4[IPv4]
    Network --> IPv6[IPv6]
    Network --> NAT[NAT]
    Network --> Subnetting[Subnetting]

    Networks --> CDN[CDN]
    Networks --> LoadBalancing[Load Balancing]
    Networks --> VPN[VPN]
```

---

# 9. Cloud Computing

```mermaid
graph TD
    Cloud[Cloud Computing]

    Cloud --> IaaS[IaaS]
    Cloud --> PaaS[PaaS]
    Cloud --> SaaS[SaaS]
    Cloud --> FaaS[FaaS / Serverless]

    Cloud --> AWS[AWS]
    Cloud --> Azure[Microsoft Azure]
    Cloud --> GCP[Google Cloud]

    AWS --> EC2[EC2]
    AWS --> S3[S3]
    AWS --> Lambda[Lambda]
    AWS --> RDS[RDS]
    AWS --> EKS[EKS]

    Azure --> VMs[Azure VMs]
    Azure --> Blob[Blob Storage]
    Azure --> Functions[Azure Functions]

    GCP --> ComputeEngine[Compute Engine]
    GCP --> CloudStorage[Cloud Storage]
    GCP --> CloudFunctions[Cloud Functions]

    Cloud --> Containers[Containers]
    Containers --> Docker[Docker]
    Containers --> Kubernetes[Kubernetes]

    Kubernetes --> Pods[Pods]
    Kubernetes --> Services[Services]
    Kubernetes --> Deployments[Deployments]
    Kubernetes --> Ingress[Ingress]

    Cloud --> Scalability[Scalability]
    Cloud --> Availability[Availability]
    Cloud --> Elasticity[Elasticity]
```

---

# 10. DevOps, CI/CD & Infrastructure

```mermaid
graph TD
    DevOps[DevOps / Platform Engineering]

    DevOps --> CI[Continuous Integration]
    DevOps --> CD[Continuous Delivery / Deployment]
    DevOps --> IaC[Infrastructure as Code]
    DevOps --> Monitoring[Monitoring]
    DevOps --> Observability[Observability]
    DevOps --> Containers[Containers]

    CI --> GitHubActions[GitHub Actions]
    CI --> Jenkins[Jenkins]
    CI --> GitLabCI[GitLab CI]

    CD --> ArgoCD[Argo CD]
    CD --> Spinnaker[Spinnaker]

    IaC --> Terraform[Terraform]
    IaC --> Ansible[Ansible]
    IaC --> CloudFormation[CloudFormation]

    Containers --> Docker[Docker]
    Containers --> Kubernetes[Kubernetes]

    Monitoring --> Prometheus[Prometheus]
    Monitoring --> Grafana[Grafana]
    Observability --> OpenTelemetry[OpenTelemetry]
    Observability --> Logging[Logging]
    Observability --> Tracing[Distributed Tracing]

    DevOps --> SRE[Site Reliability Engineering]
    SRE --> SLO[SLO]
    SRE --> SLA[SLA]
    SRE --> SLI[SLI]
```

---

# 11. Artificial Intelligence & Machine Learning

```mermaid
graph TD
    AI[Artificial Intelligence]

    AI --> ML[Machine Learning]
    AI --> DL[Deep Learning]
    AI --> NLP[NLP]
    AI --> CV[Computer Vision]
    AI --> RL[Reinforcement Learning]
    AI --> GenAI[Generative AI]

    ML --> Supervised[Supervised Learning]
    ML --> Unsupervised[Unsupervised Learning]
    ML --> SemiSupervised[Semi-Supervised Learning]
    ML --> SelfSupervised[Self-Supervised Learning]

    Supervised --> Regression[Regression]
    Supervised --> Classification[Classification]
    Unsupervised --> Clustering[Clustering]
    Unsupervised --> DimReduction[Dimensionality Reduction]

    ML --> LinearRegression[Linear Regression]
    ML --> LogisticRegression[Logistic Regression]
    ML --> DecisionTree[Decision Trees]
    ML --> RandomForest[Random Forest]
    ML --> SVM[Support Vector Machine]
    ML --> KNN[KNN]
    ML --> XGBoost[XGBoost]

    DL --> NeuralNetworks[Neural Networks]
    NeuralNetworks --> CNN[CNN]
    NeuralNetworks --> RNN[RNN]
    NeuralNetworks --> LSTM[LSTM]
    NeuralNetworks --> Transformer[Transformer]

    ML --> Features[Feature Engineering]
    ML --> Training[Model Training]
    ML --> Evaluation[Model Evaluation]
    Evaluation --> Precision[Precision]
    Evaluation --> Recall[Recall]
    Evaluation --> F1[F1 Score]
    Evaluation --> ROC[ROC-AUC]

    DL --> PyTorch[PyTorch]
    DL --> TensorFlow[TensorFlow]
    DL --> Keras[Keras]
```

---

# 12. Generative AI, LLMs & AI Engineering

```mermaid
graph TD
    GenAI[Generative AI]

    GenAI --> LLM[Large Language Models]
    GenAI --> VLM[Vision Language Models]
    GenAI --> Diffusion[Diffusion Models]
    GenAI --> Multimodal[Multimodal AI]
    GenAI --> Agents[AI Agents]

    LLM --> Transformer[Transformer]
    Transformer --> Attention[Attention]
    Transformer --> SelfAttention[Self Attention]
    Transformer --> Encoder[Encoder]
    Transformer --> Decoder[Decoder]

    LLM --> Pretraining[Pretraining]
    LLM --> FineTuning[Fine Tuning]
    LLM --> PEFT[Parameter Efficient Fine Tuning]
    PEFT --> LoRA[LoRA]
    PEFT --> QLoRA[QLoRA]

    LLM --> PromptEngineering[Prompt Engineering]
    LLM --> RAG[Retrieval Augmented Generation]
    LLM --> Embeddings[Embeddings]
    LLM --> VectorDB[Vector Databases]

    VectorDB --> FAISS[FAISS]
    VectorDB --> Pinecone[Pinecone]
    VectorDB --> Weaviate[Weaviate]
    VectorDB --> Milvus[Milvus]
    VectorDB --> Chroma[Chroma]

    RAG --> Retrieval[Retrieval]
    RAG --> Reranking[Reranking]
    RAG --> Context[Context Construction]
    RAG --> Generation[Generation]

    Agents --> Tools[Tool Calling]
    Agents --> Planning[Planning]
    Agents --> Memory[Agent Memory]
    Agents --> MCP[Model Context Protocol]
```

---

# 13. Natural Language Processing

```mermaid
graph TD
    NLP[Natural Language Processing]

    NLP --> TextProcessing[Text Processing]
    NLP --> Linguistics[Linguistics]
    NLP --> InformationRetrieval[Information Retrieval]
    NLP --> LanguageModels[Language Models]

    TextProcessing --> Tokenization[Tokenization]
    TextProcessing --> Stemming[Stemming]
    TextProcessing --> Lemmatization[Lemmatization]
    TextProcessing --> NER[Named Entity Recognition]
    TextProcessing --> POS[Part of Speech Tagging]

    NLP --> Sentiment[Sentiment Analysis]
    NLP --> Classification[Text Classification]
    NLP --> Summarization[Summarization]
    NLP --> Translation[Machine Translation]
    NLP --> QA[Question Answering]
    NLP --> InformationExtraction[Information Extraction]

    LanguageModels --> BERT[BERT]
    LanguageModels --> GPT[GPT]
    LanguageModels --> T5[T5]
    LanguageModels --> LLM

    NLP --> HuggingFace[Hugging Face]
    NLP --> SpaCy[spaCy]
    NLP --> NLTK[NLTK]
```

---

# 14. Computer Vision

```mermaid
graph TD
    CV[Computer Vision]

    CV --> ImageProcessing[Image Processing]
    CV --> Classification[Image Classification]
    CV --> Detection[Object Detection]
    CV --> Segmentation[Image Segmentation]
    CV --> OCR[OCR]
    CV --> Video[Video Understanding]

    ImageProcessing --> OpenCV[OpenCV]
    ImageProcessing --> PIL[Pillow]

    Detection --> YOLO[YOLO]
    Detection --> FasterRCNN[Faster R-CNN]
    Detection --> DETR[DETR]

    Segmentation --> UNet[U-Net]
    Segmentation --> SAM[Segment Anything]

    OCR --> Tesseract[Tesseract]
    OCR --> PaddleOCR[PaddleOCR]
    OCR --> EasyOCR[EasyOCR]

    CV --> CNN[CNN]
    CV --> VisionTransformer[Vision Transformer]
    CV --> CLIP[CLIP]
    CV --> VLM
```

---

# 15. Data Science & Data Engineering

```mermaid
graph TD
    Data[Data Science & Engineering]

    Data --> Collection[Data Collection]
    Data --> ETL[ETL / ELT]
    Data --> Processing[Data Processing]
    Data --> Analytics[Analytics]
    Data --> Visualization[Visualization]
    Data --> ML[Machine Learning]

    ETL --> Batch[Batch Processing]
    ETL --> Streaming[Streaming]

    Processing --> Pandas[Pandas]
    Processing --> NumPy[NumPy]
    Processing --> Spark[Apache Spark]
    Processing --> Polars[Polars]

    Streaming --> Kafka[Apache Kafka]
    Streaming --> Flink[Apache Flink]

    Analytics --> BI[Business Intelligence]
    BI --> PowerBI[Power BI]
    BI --> Tableau[Tableau]

    Visualization --> Matplotlib[Matplotlib]
    Visualization --> Plotly[Plotly]

    Data --> DataWarehouse[Data Warehouse]
    DataWarehouse --> Snowflake[Snowflake]
    DataWarehouse --> BigQuery[BigQuery]
    DataWarehouse --> Redshift[Amazon Redshift]
```

---

# 16. Cybersecurity

```mermaid
graph TD
    Cyber[Cybersecurity]

    Cyber --> CIA[CIA Triad]
    CIA --> Confidentiality[Confidentiality]
    CIA --> Integrity[Integrity]
    CIA --> Availability[Availability]

    Cyber --> Cryptography[Cryptography]
    Cryptography --> Symmetric[Symmetric Encryption]
    Cryptography --> Asymmetric[Asymmetric Encryption]
    Cryptography --> Hashing[Cryptographic Hashing]
    Cryptography --> PKI[Public Key Infrastructure]

    Cyber --> NetworkSecurity[Network Security]
    NetworkSecurity --> Firewall[Firewall]
    NetworkSecurity --> IDS[IDS]
    NetworkSecurity --> IPS[IPS]
    NetworkSecurity --> VPN[VPN]

    Cyber --> ApplicationSecurity[Application Security]
    ApplicationSecurity --> OWASP[OWASP]
    ApplicationSecurity --> SQLInjection[SQL Injection]
    ApplicationSecurity --> XSS[XSS]
    ApplicationSecurity --> CSRF[CSRF]
    ApplicationSecurity --> Auth[Authentication]
    ApplicationSecurity --> Authorization[Authorization]

    Auth --> OAuth[OAuth]
    Auth --> OpenID[OpenID Connect]
    Authorization --> RBAC[RBAC]
    Authorization --> ABAC[ABAC]

    Cyber --> PenTesting[Penetration Testing]
    Cyber --> ThreatModeling[Threat Modeling]
    Cyber --> ZeroTrust[Zero Trust]
```

---

# 17. Distributed Systems

```mermaid
graph TD
    DS[Distributed Systems]

    DS --> Communication[Distributed Communication]
    DS --> Consensus[Consensus]
    DS --> Replication[Replication]
    DS --> Partitioning[Partitioning]
    DS --> FaultTolerance[Fault Tolerance]
    DS --> Consistency[Consistency]
    DS --> Scalability[Scalability]

    Communication --> RPC[RPC]
    RPC --> GRPC[gRPC]
    Communication --> Messaging[Message Queues]
    Messaging --> Kafka[Kafka]
    Messaging --> RabbitMQ[RabbitMQ]

    Consensus --> Paxos[Paxos]
    Consensus --> Raft[Raft]

    Consistency --> StrongConsistency[Strong Consistency]
    Consistency --> EventualConsistency[Eventual Consistency]
    Consistency --> CAP[CAP Theorem]

    Replication --> LeaderFollower[Leader-Follower]
    Replication --> MultiLeader[Multi-Leader]
    Replication --> Leaderless[Leaderless]

    FaultTolerance --> Retry[Retries]
    FaultTolerance --> CircuitBreaker[Circuit Breaker]
    FaultTolerance --> Failover[Failover]
```

---

# 18. Mobile Development

```mermaid
graph TD
    Mobile[Mobile Development]

    Mobile --> Android[Android]
    Mobile --> iOS[iOS]
    Mobile --> CrossPlatform[Cross Platform]

    Android --> Kotlin[Kotlin]
    Android --> Jetpack[Android Jetpack]
    Android --> Compose[Jetpack Compose]

    iOS --> Swift[Swift]
    iOS --> SwiftUI[SwiftUI]

    CrossPlatform --> Flutter[Flutter]
    CrossPlatform --> ReactNative[React Native]
    CrossPlatform --> Expo[Expo]

    Mobile --> Push[Push Notifications]
    Mobile --> Offline[Offline First]
    Mobile --> MobileSecurity[Mobile Security]
    Mobile --> AppStore[App Distribution]
```

---

# 19. Embedded Systems, IoT & Robotics

```mermaid
graph TD
    Embedded[Embedded Systems]

    Embedded --> Microcontrollers[Microcontrollers]
    Embedded --> RTOS[Real Time Operating Systems]
    Embedded --> Firmware[Firmware]
    Embedded --> Sensors[Sensors]
    Embedded --> Actuators[Actuators]

    Microcontrollers --> Arduino[Arduino]
    Microcontrollers --> ESP32[ESP32]
    Microcontrollers --> STM32[STM32]
    Microcontrollers --> RaspberryPi[Raspberry Pi]

    RTOS --> FreeRTOS[FreeRTOS]
    RTOS --> Zephyr[Zephyr]

    IoT[Internet of Things] --> Embedded
    IoT --> MQTT[MQTT]
    IoT --> EdgeComputing[Edge Computing]
    IoT --> IoTCloud[IoT Cloud]

    Robotics[Robotics] --> ROS[ROS]
    Robotics --> Sensors
    Robotics --> ComputerVision[Computer Vision]
    Robotics --> ControlSystems[Control Systems]
```

---

# 20. Blockchain & Distributed Ledger

```mermaid
graph TD
    Blockchain[Blockchain]

    Blockchain --> DistributedLedger[Distributed Ledger]
    Blockchain --> Cryptography[Cryptography]
    Blockchain --> Consensus[Consensus]
    Blockchain --> SmartContracts[Smart Contracts]

    Consensus --> PoW[Proof of Work]
    Consensus --> PoS[Proof of Stake]
    Consensus --> BFT[Byzantine Fault Tolerance]

    SmartContracts --> Ethereum[Ethereum]
    SmartContracts --> Solidity[Solidity]
    Ethereum --> EVM[Ethereum Virtual Machine]

    Blockchain --> Bitcoin[Bitcoin]
    Blockchain --> Web3[Web3]
    Web3 --> Wallets[Wallets]
    Web3 --> DeFi[DeFi]
    Web3 --> DAOs[DAOs]
```

---

# 21. Computer Graphics, HCI & Game Development

```mermaid
graph TD
    Graphics[Computer Graphics]

    Graphics --> Rendering[Rendering]
    Graphics --> Modeling[3D Modeling]
    Graphics --> Animation[Animation]
    Graphics --> Shaders[Shaders]
    Graphics --> GPU[GPU]

    Rendering --> Rasterization[Rasterization]
    Rendering --> RayTracing[Ray Tracing]
    Shaders --> GLSL[GLSL]
    Graphics --> OpenGL[OpenGL]
    Graphics --> Vulkan[Vulkan]
    Graphics --> DirectX[DirectX]

    GameDev[Game Development] --> Unity[Unity]
    GameDev --> Unreal[Unreal Engine]
    GameDev --> Physics[Game Physics]
    GameDev --> GameAI[Game AI]

    HCI[Human Computer Interaction] --> UX[UX]
    HCI --> UI[UI]
    HCI --> Accessibility[Accessibility]
    HCI --> Usability[Usability]
    HCI --> InteractionDesign[Interaction Design]
```

---

# 22. Theory of Computation

```mermaid
graph TD
    Theory[Theory of Computation]

    Theory --> Automata[Automata Theory]
    Theory --> FormalLanguages[Formal Languages]
    Theory --> Computability[Computability]
    Theory --> ComplexityTheory[Complexity Theory]

    Automata --> DFA[DFA]
    Automata --> NFA[NFA]
    Automata --> PDA[Pushdown Automata]
    Automata --> TM[Turing Machine]

    FormalLanguages --> RegularLanguages[Regular Languages]
    FormalLanguages --> CFG[Context Free Grammars]

    Computability --> Decidability[Decidability]
    Computability --> Halting[Halting Problem]

    ComplexityTheory --> P[Class P]
    ComplexityTheory --> NP[Class NP]
    ComplexityTheory --> NPComplete[NP Complete]
    ComplexityTheory --> NPHard[NP Hard]
```

---

# 23. Compilers & Programming Language Implementation

```mermaid
graph TD
    Compiler[Compiler Design]

    Compiler --> Lexical[Lexical Analysis]
    Compiler --> Parsing[Parsing]
    Compiler --> Semantic[Semantic Analysis]
    Compiler --> IR[Intermediate Representation]
    Compiler --> Optimization[Optimization]
    Compiler --> CodeGeneration[Code Generation]

    Lexical --> Lexer[Lexer]
    Parsing --> Parser[Parser]
    Parsing --> CFG[Context Free Grammar]

    Parser --> AST[Abstract Syntax Tree]
    Semantic --> TypeChecking[Type Checking]
    IR --> SSA[Static Single Assignment]
    Optimization --> DeadCode[Dead Code Elimination]
    Optimization --> ConstantFolding[Constant Folding]
    CodeGeneration --> MachineCode[Machine Code]
    CodeGeneration --> Assembly[Assembly]

    Compiler --> LLVM[LLVM]
    Compiler --> GCC[GCC]
```

---

# 24. Common Cross-Domain Relationships

```mermaid
graph LR
    Python --> ML[Machine Learning]
    Python --> DataScience[Data Science]
    Python --> Backend[Backend]
    Python --> Automation[Automation]

    C++ --> Systems[Systems]
    C++ --> GameDev[Game Development]
    C++ --> CompetitiveProgramming[Competitive Programming]

    Java --> Enterprise[Enterprise Software]
    Java --> Android[Android]
    Java --> Backend

    JavaScript --> Frontend[Frontend]
    JavaScript --> Node[Node.js]
    TypeScript --> Frontend
    TypeScript --> Backend

    SQL --> RelationalDB[Relational Databases]
    Docker --> DevOps[DevOps]
    Kubernetes --> Cloud[Cloud]
    Git --> CI[CI/CD]
    Linux --> Cloud
    Linux --> DevOps
    Linux --> Cybersecurity[Cybersecurity]

    TensorFlow --> DeepLearning[Deep Learning]
    PyTorch --> DeepLearning
    HuggingFace --> NLP
    HuggingFace --> LLM[LLMs]

    Kafka --> DistributedSystems[Distributed Systems]
    Kafka --> DataEngineering[Data Engineering]

    REST --> Web
    GraphQL --> Web
    gRPC --> Microservices[Microservices]

    Redis --> Caching[Caching]
    PostgreSQL --> Backend
    MongoDB --> Backend

    AWS --> Cloud
    Azure --> Cloud
    GCP --> Cloud
```

---

# 25. Concept Dependency Graph

This graph shows a **learning dependency relationship**, rather than merely a technology relationship.

```mermaid
graph TD
    Programming[Programming Fundamentals]
    DSA[Data Structures & Algorithms]
    Math[Math & Discrete Mathematics]
    OS[Operating Systems]
    Networks[Computer Networks]
    DB[Databases]
    Architecture[Computer Architecture]

    Programming --> DSA
    Math --> DSA
    Programming --> OS
    Programming --> DB
    Programming --> Networks
    Architecture --> OS

    DSA --> Algorithms[Advanced Algorithms]
    OS --> Distributed[Distributed Systems]
    Networks --> Distributed
    DB --> Distributed

    Programming --> Web[Web Development]
    Networks --> Web
    DB --> Backend[Backend Engineering]
    OS --> Backend

    Math --> ML[Machine Learning]
    DSA --> ML
    Programming --> ML
    ML --> DeepLearning[Deep Learning]
    DeepLearning --> NLP[NLP]
    DeepLearning --> ComputerVision[Computer Vision]
    DeepLearning --> GenAI[Generative AI]

    OS --> Cloud[Cloud Computing]
    Networks --> Cloud
    Distributed --> Cloud
    Web --> Cloud

    Cloud --> DevOps[DevOps]
    DevOps --> Kubernetes[Kubernetes]
    Cloud --> Microservices[Microservices]
    Distributed --> Microservices
```

---

# 26. CSE Technology Stack Map

```mermaid
graph TD
    User[User]
    UI[UI / UX]
    Frontend[Frontend]
    API[API Layer]
    Backend[Backend]
    Cache[Cache]
    DB[Database]
    Queue[Message Queue]
    ML[ML / AI Services]
    Storage[Object Storage]
    Infra[Infrastructure]
    Cloud[Cloud]
    Monitoring[Observability]

    User --> UI
    UI --> Frontend
    Frontend --> API
    API --> Backend

    Backend --> Cache
    Backend --> DB
    Backend --> Queue
    Backend --> ML
    Backend --> Storage

    Queue --> ML
    DB --> ML
    Storage --> ML

    Backend --> Infra
    ML --> Infra
    DB --> Infra
    Queue --> Infra

    Infra --> Cloud
    Cloud --> Monitoring
    Backend --> Monitoring
    ML --> Monitoring
```

---

# 27. Suggested Graph Data Model

To turn this document into an interactive knowledge graph, represent each concept as a node:

```text
Node:
  id
  name
  category
  description
  difficulty
  aliases
  technologies
  prerequisites
  resources

Edge:
  source
  target
  relation
  weight
```

Example:

```text
Python
  category: Programming Language

Python --parent--> Programming Languages
Python --used-by--> Machine Learning
Python --used-by--> Data Science
Python --used-by--> Backend Development
Python --related--> Automation
```

Recommended `relation` values:

```text
parent
child
related
builds-on
prerequisite
implements
used-by
alternative
part-of
specialization-of
depends-on
```

---

# 28. Recommended Top-Level Taxonomy

The complete CSE graph can therefore be organized into these major parent nodes:

1. Programming & Languages
2. Data Structures & Algorithms
3. Discrete Mathematics & Theory
4. Computer Architecture
5. Operating Systems
6. Computer Networks
7. Databases & Data Management
8. Software Engineering
9. Web Development
10. Mobile Development
11. Cloud Computing
12. DevOps & Infrastructure
13. Distributed Systems
14. Artificial Intelligence
15. Machine Learning
16. Deep Learning
17. NLP
18. Computer Vision
19. Generative AI & LLMs
20. Data Science
21. Data Engineering
22. Cybersecurity
23. Cryptography
24. Embedded Systems
25. IoT
26. Robotics
27. Blockchain
28. Computer Graphics
29. Game Development
30. HCI / UX
31. Compilers
32. Parallel & High Performance Computing
33. Quantum Computing
34. Bioinformatics / Computational Biology
35. Information Retrieval
36. Search Systems
37. Software Architecture
38. Testing & Quality Engineering
39. Reliability / SRE
40. AI Engineering / MLOps

---

# 29. Important Note

This is intended as a **CSE knowledge graph**, not simply a list of technologies. In a full implementation, a single node can belong to multiple graphs simultaneously.

For example:

```text
Python
 ├── Programming Language
 ├── Scripting
 ├── Backend Development
 ├── Data Science
 ├── Machine Learning
 ├── AI Engineering
 ├── Automation
 └── DevOps tooling
```

Likewise:

```text
Kubernetes
 ├── Cloud Computing
 ├── Containers
 ├── DevOps
 ├── Distributed Systems
 ├── Microservices
 ├── Networking
 └── Site Reliability Engineering
```

This overlapping structure is intentional: **CSE concepts are highly interconnected rather than mutually exclusive.**
