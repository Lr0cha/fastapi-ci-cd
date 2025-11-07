<div align="center">

# GitOps com Kubernetes, Rancher Desktop e ArgoCD

![ArgoCD](https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white)
![GitOps](https://img.shields.io/badge/GitOps-FF6B6B?style=for-the-badge&logo=git&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Rancher](https://img.shields.io/badge/Rancher_Desktop-0075A8?style=for-the-badge&logo=rancher&logoColor=white)
![Github Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
</div>

Este projeto implementa uma pipeline **GitOps** completa. Ele automatiza o ciclo de **desenvolvimento, build, deploy e execução** de uma aplicação **FastAPI (CRUD de Produtos)**, utilizando:

  * **GitHub Actions** para CI/CD (Build e Push de Imagem).
  * **Docker Hub** como Registry de Imagens.
  * **ArgoCD** para Entrega Contínua (CD) e sincronização do estado desejado.
  * **Kubernetes local** via **Rancher Desktop**.

O fluxo é baseado no princípio GitOps:

* 1️⃣ **Código** (App) é alterado e o push é feito.
* 2️⃣ **GitHub Actions** faz o **Build** da nova imagem Docker e o **Push** para o Docker Hub.
* 3️⃣ O workflow, em seguida, atualiza o *Manifest de Deploy* no **Repositório de Manifests** e faz o push da alteração.
* 4️⃣ **ArgoCD** detecta a alteração no *Manifest* (nova tag de imagem) e automaticamente sincroniza o cluster Kubernetes (Rancher Desktop), atualizando para nova versão da aplicação.


## 🛠️ Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas e configuradas:

  * **Conta no GitHub** (repositórios públicos).
  * **Conta no Docker Hub** com **Token de Acesso** para escrita.
  * **Rancher Desktop** com Kubernetes habilitado.
  * `kubectl` configurado corretamente (`kubectl get nodes`).
  * **ArgoCD** instalado no cluster local.
  * **Git**, **Python 3** e **Docker** instalados localmente.


## 🔒 Configuração de Segredos (Secrets)

Para que o **GitHub Actions** possa fazer o push para o Docker Hub e acessar o **Repositório de Manifests** via SSH, configure os seguintes *Secrets* no seu repositório GitHub (Settings -\> Secrets and variables -\> Actions):

| Nome do Secret | Propósito |
| :--- | :--- |
| `DOCKER_HUB_USERNAME` | Seu nome de usuário do Docker Hub. |
| `DOCKER_HUB_TOKEN` | Token de Acesso e com direito de escrita gerado no Docker Hub. |
| `SSH_PRIVATE_ACCESS_KEY` | Chave privada SSH para acesso de escrita ao repositório de manifests. |

**Passos para Configuração:**

1.  **Gerar Token no Docker Hub:** Acessar Configurações $\rightarrow$ Personal Access Token.
   
<div align="center">
  <img alt="Token Docker Hub" src="https://github.com/user-attachments/assets/a053c725-4159-44cc-aab6-dab9a43681e1"/>
  <br />
  <i>Figura 1 - Geração do Token com write access do Docker Hub</i>
</div>

2.  **Configurar Secrets no GitHub:**
      * `DOCKER_HUB_USERNAME` $\rightarrow$ `[seu-usuario-docker]`
      * `DOCKER_HUB_TOKEN` $\rightarrow$ `[token-docker-hub]`
      * **Criar Chave SSH:** Gerar par de chaves SSH no seu ambiente local (ssh-keygen -t ed25519 -C "string").
      * `SSH_PRIVATE_ACCESS_KEY` $\rightarrow$ `[chave-privada]`
      * **Adicionar Chave Pública:** Adicionar a chave pública (.pub) como **Deploy Key** no seu **Repositório de Manifests** com permissão de escrita.
<div align="center">
  <img alt="SSH Public Key" src="https://github.com/user-attachments/assets/48d093ef-1c69-4bff-a271-9d2446dc5988"/>
  <br />
  <i>Figura 2 - Configurando deploy key</i>
</div>

## 📂 Estrutura do Repositório de Manifests

Este projeto utiliza um repositório separado [fastapi-k8s-manifests](https://github.com/Lr0cha/fastapi-k8s-manifests) para armazenar os manifests Kubernetes, seguindo a prática GitOps:

```
fastapi-deployment.yaml
fastapi-service.yaml
```


## Instalação e Configuração

### 1\. Instalação e Acesso ao ArgoCD

Garanta que o Kubernetes esteja em execução (`kubectl get nodes`).

  * **Instalar ArgoCD:**
    ```bash
    kubectl create namespace argocd
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    ```
  * **Acesso à UI e Senha Inicial (usuário: `admin`):**
    ```bash
    # Expor o serviço localmente
    kubectl port-forward svc/argocd-server -n argocd 8080:443 &

    # Obter a senha inicial
    kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
    ```
    > **Acesso:** 🔗 https://localhost:8080

### 2\. Criar a Aplicação no ArgoCD (CLI)

Utilize o `argocd` CLI para criar a aplicação, apontando para o seu **Repositório de Manifests**.

  * **Login no ArgoCD Server:**
    ```bash
    argocd login localhost:8080 --insecure
    # Usuário: admin, Senha: <obtida acima>
    ```
  * **Criação da Aplicação:**
    Substitua `<SEU_USER>` e `<SEU_REPO_MANIFESTS>`:
    ```bash
    argocd app create fastapi-app \
      --repo https://github.com/<SEU_USER>/<SEU_REPO_MANIFESTS>.git \
      --path . \
      --dest-server https://kubernetes.default.svc \
      --dest-namespace default \
      --revision HEAD \
      --sync-policy automatic
    ```

> [!NOTE]
>  O ArgoCD iniciará o processo de sincronização (Sync) dos manifests do repositório para o seu cluster local.

<div align="center">
  <img alt="Argo CD" src="https://github.com/user-attachments/assets/6eb17fd5-fe6e-4a63-9606-8be9ef429e84"/>
  <br />
  <i>Figura 3 - ArgoCD autoSync</i>
</div>

No Docker Hub:

<div align="center">
  <img alt="Docker Hub" src="https://github.com/user-attachments/assets/994cc439-09d1-4edf-a409-98f011774316"/>
  <br />
  <i>Figura 4 - Imagem no Docker Hub</i>
</div>

-----

## ⚙️ Workflow do GitHub Actions (`.github/workflows/main.yaml`)

O workflow é composto por dois Jobs: `build-and-push` e `update-manifest`, garantindo o fluxo completo de CI/CD e GitOps.

### Pipeline CI/CD

```yaml
name: CI/CD Pipeline - Build, Push FastAPI Application

on:
  workflow_dispatch: 
  push:
    branches:
      - main 
    paths-ignore:
      - '**.md'

env:
  DOCKER_REPO: ${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-app
  MANIFEST_FILE_PATH: manifests/fastapi-deployment.yaml 

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      # ... (Passos de Checkout, Login no Docker Hub, Build e Push da Imagem)
      - name: Build and Push Docker Image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          tags: |
            ${{env.DOCKER_REPO}}:v${{github.run_number}}
            ${{ secrets.DOCKER_HUB_USERNAME }}/fastapi-app:latest

  update-manifest:
    runs-on: ubuntu-latest
    needs: build-and-push
    steps:
      - name: Checkout Manifests Repository
        uses: actions/checkout@v5
        with:
          # Repositório separado para manifests
          repository: ${{ github.repository_owner }}/fastapi-k8s-manifests
          ssh-key: ${{ secrets.SSH_PRIVATE_ACCESS_KEY }}
          path: manifests
          
      - name: Update deployment tag and Push
        run: |
          NEW_TAG="${{ env.DOCKER_REPO }}:v${{ github.run_number }}"
          echo "Nova Imagem: $NEW_TAG"
          
          cd manifests
          # Atualiza a tag da imagem no Deployment
          sed -i "s|image: .*/fastapi-app:.*|image: ${NEW_TAG}|" fastapi-deployment.yaml
          
          git config --global user.name "GitHub Actions"
          git config --global user.email "actions@github.com"
          git add .

          git commit -m "chore(image): update FastAPI image version to v${{ github.run_number }}"
          git push origin main
```

## 📷 Resultados da Execução

### Após o push do código da aplicação, o workflow é executado com sucesso:

<div align="center">
  <img alt="Workflow" src="https://github.com/user-attachments/assets/bafe0989-31f9-4120-8339-1421ef16d9b9"/>
  <br />
  <i>Figura 5 - Workflow do GitHub Actions com status de sucesso</i>
</div>

### A alteração da tag é sincronizada pelo ArgoCD, gerando o Rollout da nova versão:

<div align="center">
  <img alt="Rollout" src="https://github.com/user-attachments/assets/a4aa4f7e-3b9f-4f9f-a946-d72cf86f4dbe"/>
  <br />
  <i>Figura 6 - Imagem da Aplicação no ArgoCD UI no estado Sincronizado após o Rollout</i>
</div>

### O commit de atualização da tag é visível no repositório de manifests:

<div align="center">
  <img alt="Manifests log" src="https://github.com/user-attachments/assets/fd64174c-b37e-4d47-8a09-75cdb7a2e5c9"/>
  <br />
  <i>Figura 7 - Commit no Repositório de Manifests</i>
</div>

### Status dos Pods no Kubernetes:

<div align="center">
  <img alt="kubectl get pods" src="https://github.com/user-attachments/assets/70db3d5a-dc25-4ec4-a610-798c886dfd43"/>
  <br />
  <i>Figura 8 - kubectl get pods</i>
</div>

---

## ✅ Acesso à Aplicação Final

Para acessar o CRUD de Produtos rodando no seu Kubernetes local:

  * **Acesso via Port-Forward:**
    ```bash
    kubectl port-forward svc/fastapi-service 8000:8000 -n default
    ```
    
> [!NOTE]
> O port-forward permite acesso direto, sem NodePort ou LoadBalancer.

**Acesso Final:**
🔗 [http://localhost:8000](https://www.google.com/search?q=http://localhost:8000)

<div align="center">
  <img alt="FastAPI app" src="https://github.com/user-attachments/assets/9387e02d-c60b-4b6a-bf0f-186b9ad5edbc"/>
  <br />
  <i>Figura 9 - Aplicação FastAPI CRUD de Produtos rodando</i>
</div>
