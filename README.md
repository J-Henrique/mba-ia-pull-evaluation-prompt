### Status dos entregáveis (preenchido)

- ✅ **Prompt otimizado criado e publicado:** `prompts/bug_to_user_story_v2.yml` e `jhbbortolotto/bug_to_user_story_v2`
- ✅ **Scripts implementados e funcionais:** `src/pull_prompts.py`, `src/push_prompts.py`, `src/evaluate.py`
- ✅ **Resultados finais ≥ 0.9 em todas as métricas** (detalhes na seção **Resultados Finais**)
- ✅ **Tabela comparativa v1 vs v2** incluída neste README
- ✅ **Seção Técnicas Aplicadas (Fase 2)** preenchida com racional das técnicas e critérios
- ✅ **Seção Como Executar** preenchida neste README (ver seção abaixo)

### Links e evidências para submissão

- **Prompt no LangSmith Hub:** https://smith.langchain.com/hub/jhbbortolotto/bug_to_user_story_v2
- **Repositório no GitHub:** https://github.com/J-Henrique/mba-ia-pull-evaluation-prompt

---

## Como Executar

### Pré-requisitos

- Python 3.9+
- Conta no LangSmith e API key configurada
- Chave de provedor LLM (OpenAI ou Google)

### Setup

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Execução do fluxo completo

```bash
# 1) Pull do prompt inicial
python src/pull_prompts.py

# 2) Editar prompt otimizado
# arquivo: prompts/bug_to_user_story_v2.yml

# 3) Push do prompt otimizado para o Hub
python src/push_prompts.py

# 4) Avaliação final
python src/evaluate.py

# 5) Testes de validação
pytest tests/test_prompts.py
```

---

## Técnicas Aplicadas (Fase 2)

### Técnicas escolhidas

- **Role Prompting**: definição explícita de persona (Senior Product Manager) para manter tom profissional, empático e orientado a valor.
- **Few-shot Learning**: inclusão de exemplos de entrada/saída com estrutura-alvo para estabilizar formato e qualidade dos critérios.
- **Skeleton of Thought (estruturado)**: instruções internas de checklist e ordem de construção para garantir cobertura completa do bug antes da resposta final.

### Exemplos práticos de aplicação

- **Role Prompting (aplicação prática):** o system prompt foi ajustado para instruir o modelo a responder como *Senior Product Manager*, priorizando linguagem colaborativa e foco em valor ao usuário em vez de descrição técnica fria do defeito.
- **Few-shot Learning (aplicação prática):** foram adicionados exemplos de bug report convertidos para user stories no formato alvo, com critérios em Dado/Quando/Então, para reduzir variação de estrutura entre respostas.
- **Skeleton of Thought (aplicação prática):** o prompt passou a exigir sequência de montagem (extrair contexto/impacto → redigir user story → gerar critérios testáveis → checar completude), evitando omissões de plataforma, condições e resultado observável.

### O que é esperado em cada critério de avaliação

- **Tone Score**: linguagem profissional, empática e positiva, com foco no valor para o usuário (não apenas “corrigir bug”).
- **Acceptance Criteria Score**: critérios claros, testáveis, estruturados (Dado/Quando/Então), com cobertura adequada do cenário.
- **User Story Format Score**: aderência ao formato “Como..., eu quero..., para que...”, com persona, ação e benefício explícitos.
- **Completeness Score**: cobertura de todos os detalhes do bug (contexto técnico, impacto, plataforma, comportamento esperado e validações observáveis).

### Por que o segundo prompt funcionou melhor que o primeiro

Na primeira versão otimizada, já havia bom desempenho em tom, formato e critérios, mas ainda com lacunas de **completude** em alguns casos (especialmente quando o bug exigia mais contexto técnico e validação de resultado).

No segundo ajuste, foram adicionadas regras explícitas para:

- Cobrir **todos os detalhes citados** no bug (plataforma, navegador, números e condições);
- Refletir **impacto/severidade** no benefício e em critérios de aceitação;
- Incluir validações de resultado **observável** (estado de UI, consistência de dados, prevenção de regressão);
- Executar um **checklist de completude** antes de responder.

Esse ajuste elevou especificamente o **Completeness Score**, mantendo os demais critérios altos.

---

## Resultados Finais

### Execução aprovada (prompt final)

- **Prompt publicado:** `jhbbortolotto/bug_to_user_story_v2`
- **Projeto no LangSmith:** `prompt-optimization-challenge-resolved`
- **Status final:** ✅ **APROVADO**

### Métricas finais

- Tone Score: **0.98**
- Acceptance Criteria Score: **0.97**
- User Story Format Score: **0.98**
- Completeness Score: **0.91**
- **Média Geral:** **0.9610**

### Comparação de iterações (resumo)

| Iteração | Tone | Acceptance | Format | Completeness | Média | Status |
|----------|------|------------|--------|--------------|-------|--------|
| Prompt otimizado (1ª versão) | 0.98 | 0.96 | 0.99 | 0.80 | 0.9334 | ❌ Reprovado |
| Prompt otimizado (2ª versão, refinada) | 0.98 | 0.97 | 0.98 | 0.91 | 0.9610 | ✅ Aprovado |

> Observação: a 1ª versão já tinha média alta, mas reprova pela regra do desafio exigir **todas** as métricas ≥ 0.9.
