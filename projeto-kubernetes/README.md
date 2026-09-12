# 🚀 Projeto 1 — Nginx com Kubernetes

## 📌 Sobre o projeto

Projeto prático desenvolvido para estudar os fundamentos do Kubernetes utilizando o Nginx como aplicação de exemplo.

O projeto demonstra a criação e gerenciamento de Pods através de um **Deployment**, exposição da aplicação utilizando um **Service** e recuperação automática de um Pod após sua remoção.

## 🎯 Objetivos

* Compreender a estrutura básica do Kubernetes.
* Criar um Deployment utilizando YAML.
* Executar múltiplas réplicas de uma aplicação.
* Criar um Service para acessar os Pods.
* Utilizar `kubectl` para administrar os recursos.
* Entender o conceito de estado desejado.
* Observar a recuperação automática de Pods.

## 🛠️ Tecnologias utilizadas

* Kubernetes
* Docker Desktop
* Nginx
* YAML
* kubectl
* PowerShell
* VS Code

## 📁 Estrutura do projeto

```text
projeto-kubernetes/
├── deployment.yaml
├── service.yaml
└── README.md
```

## ⚙️ Deployment

O arquivo `deployment.yaml` define um Deployment chamado `nginx-deployment`.

O projeto utiliza:

* 3 réplicas do Nginx
* Imagem `nginx:latest`
* Container na porta 80
* Label `app: nginx`

Exemplo da configuração principal:

```yaml
replicas: 3
```

Isso informa ao Kubernetes que o estado desejado é manter **3 Pods** executando.

## 🔌 Service

O arquivo `service.yaml` cria o Service:

```text
nginx-service
```

O Service utiliza:

```yaml
selector:
  app: nginx
```

Dessa forma, ele identifica os Pods que possuem a label `app: nginx`.

O Service foi configurado como:

```text
NodePort
```

A porta atribuída pelo Kubernetes foi:

```text
30632
```

## 🌐 Acesso à aplicação

Durante o desenvolvimento, o acesso ao Nginx foi realizado através de:

```bash
kubectl port-forward service/nginx-service 8080:80
```

Depois, a aplicação foi acessada pelo navegador através de:

```text
http://localhost:8080
```

O resultado apresent
