##esse é um pedaço do código que fiz para tentar alterar a leitura de 4 colunas que apenas alguns valores estão voltando com a virgula em local errado
# apesar de descrever a coluna ele não consegue fazer essa leitura. 
## acima eu pedi para salvar apenas 2 numeros apos a virgula e ele conseguiu 

try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
            writer.writeheader()
            
            # Salvar os resultados originais
            for result in results:
                rounded_result = {}
                for key, value in result.items():
                    if isinstance(value, (int, float)) and key not in ["RTPlan", "Feixe", "Sítio"]:
                        rounded_result[key] = round(value, 2)
                    else:
                        rounded_result[key] = value
                writer.writerow({k: rounded_result.get(k, 0.0) for k in headers})

            # Tentar ler e corrigir linhas mal formatadas no final do arquivo
            with open(output_path, 'r', encoding='utf-8') as csvfile_read:
                lines = csvfile_read.readlines()
                if lines:
                    last_line = lines[-1].strip()
                    if not last_line or all(c in '0123456789. ' for c in last_line) and len(last_line.split()) == 4:
                        extra_data = []
                        for line in reversed(lines):
                            parts = line.strip().split()
                            if len(parts) == 4 and all(p.replace('.', '').isdigit() for p in parts):
                                extra_data.insert(0, {
                                    "ALS": float(parts[0]),
                                    "SLS": float(parts[1]),
                                    "ALA": float(parts[2]),
                                    "SLA": float(parts[3])
                                })
                            else:
                                break
                        for data in extra_data:
                            new_entry = {"RTPlan": "UNKNOWN", "Feixe": 0}
                            new_entry.update(data)
                            for key in headers[3:]:  # Preencher outros campos com 0 ou nulo
                                if key not in data:
                                    new_entry[key] = 0.0 if key not in ["RTPlan", "Feixe", "Sítio"] else "UNKNOWN"
                            writer.writerow({k: new_entry.get(k, 0.0) for k in headers})
                            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile_rewrite:
                                writer = csv.DictWriter(csvfile_rewrite, fieldnames=headers, extrasaction='ignore')
                                writer.writeheader()
                                for result in results + [new_entry]:
                                    rounded_result = {}
                                    for key, value in result.items():
                                        if isinstance(value, (int, float)) and key not in ["RTPlan", "Feixe", "Sítio"]:
                                            rounded_result[key] = round(value, 2)
                                        else:
                                            rounded_result[key] = value
                                    writer.writerow({k: rounded_result.get(k, 0.0) for k in headers})

        logger.info("Resultados salvos com sucesso")
    except Exception as e:
        logger.error("Falha ao salvar CSV: %s", e)

if __name__ == "__main__":
    main()

