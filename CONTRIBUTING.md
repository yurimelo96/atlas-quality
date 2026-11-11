# Contribua com Atlas

Abra uma issue descrevendo contexto, comportamento esperado, resultado observado e uma reprodução mínima sem dados sensíveis. Para alterações pequenas, envie um PR diretamente. Para novas integrações, explique o caso de uso e as permissões necessárias antes de ampliar o escopo.

Mantenha a entrada da skill curta e mova detalhes específicos para referências vinculadas. Preserve a liberdade do usuário de pular verificações e a distinção entre resultado observado e conclusão. Não adicione gates universais, números de qualidade sem evidência ou dependências sem benefício demonstrado.

Execute `python -m unittest discover -s tests -v` ao modificar o helper. Ao modificar instruções, exercite os cenários pertinentes de `docs/evaluation.md` e relate o comportamento real e suas limitações no PR. Não é necessário instalar ferramentas de pentest para contribuir com documentação.

Use dados sintéticos, trate participantes com respeito e descreva críticas em termos de comportamento observável. Contribuições são distribuídas sob a licença MIT do projeto. Não publique vulnerabilidades exploráveis ou segredos em issues; consulte SECURITY.md.
