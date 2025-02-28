"""
Author:         Pablo Andrade [github.com/pablodeas]
Description     Programa criado para manter controle de horário e horas extras.
Created:        28/02/2025
"""

import click
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("DATABASE")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_container = os.getenv("DB_CONTAINER")
db_host = os.getenv("HOST")
db_port = os.getenv("PORT")

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados"""
    try:
        conn = psycopg2.connect(
            dbname=database, 
            user=db_user, 
            password=db_password, 
            host=db_host, 
            port=int(db_port)
        )
        return conn
    except Exception as e:
        print(f"> Erro ao conectar ao banco de dados: {e}")
        return None

@click.group()
def cli():
    """> Registre suas horas extras."""
    pass

def calcular_horas_extras(hora_entrada, hora_saida):
    """
    Calcula horas extras baseado na entrada e saída.
    Jornada normal = 9 horas
    Formato de entrada esperado: 'HH:MM' (ex: '08:00', '17:30')
    Retorna o total de minutos extras como inteiro
    """
    try:
        # Converte string de tempo para objetos datetime
        from datetime import datetime, timedelta
        
        formato = "%H:%M"
        entrada = datetime.strptime(hora_entrada, formato)
        saida = datetime.strptime(hora_saida, formato)
        
        # Se a saída for antes da entrada, assume que passou para o próximo dia
        if saida < entrada:
            saida = saida + timedelta(days=1)
        
        # Calcula o total de horas trabalhadas
        duracao = saida - entrada
        total_minutos = duracao.total_seconds() / 60
        
        # Jornada normal em minutos (9 horas = 540 minutos)
        jornada_normal = 9 * 60
        
        # Calcula minutos extras
        minutos_extras = max(0, total_minutos - jornada_normal)
        
        # Retorna o total de minutos extras como inteiro
        return int(minutos_extras)
        
    except Exception as e:
        print(f"> Erro ao calcular horas extras: {e}")
        return 0

@cli.command(help="> List all.")
def list():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return
        
        cur = conn.cursor()
        cur.execute("SELECT id, to_char(hr_begin, 'HH24:MI'), to_char(hr_end, 'HH24:MI'), dia, extra FROM public.ponto ORDER BY dia ASC")
        rows = cur.fetchall()

        for i in rows:
            id_registro = i[0]
            entrada = i[1]
            saida = i[2]
            data = i[3]
            minutos_extras = i[4]
            
            # Converte minutos em formato legível
            horas = minutos_extras // 60
            minutos = minutos_extras % 60
            tempo_extra = f"{horas}h {minutos}min"
            
            print(f".id: {id_registro} | entrada: {entrada} | saida: {saida} | data: {data} | hora extra: {tempo_extra}")

    except Exception as e:
        print(f"> An error occurred: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@cli.command(help="> Insert time")
@click.argument('entrada')
@click.argument('saida')
@click.argument('data')
def insert(entrada, saida, data):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cur = conn.cursor()
        
        # Calcula horas extras em minutos (valor inteiro)
        minutos_extras = calcular_horas_extras(entrada, saida)
        
        cur.execute("""
            INSERT INTO public.ponto(hr_begin, hr_end, dia, extra)
            VALUES(%s::time, %s::time, %s, %s);
            """,
            (entrada, saida, data, minutos_extras))
        conn.commit()
        
        # Para exibição, converte minutos em formato legível
        horas = minutos_extras // 60
        minutos = minutos_extras % 60
        tempo_extra_formatado = f"{horas}h {minutos}min"
        
        print(f".Inserted -> Entrada: {entrada}, Saída: {saida}, Data: {data}, Extra: {tempo_extra_formatado}.")
                
    except Exception as e:
        print(f"> An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@cli.command(help="> Delete by Id.")
@click.argument('id', type=int)
def delete(id):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        if not conn:
            return
            
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM public.ponto WHERE id = %s;
            """,
            (id,))
        
        if cur.rowcount == 0:
            print(f".Nenhum registro encontrado com ID {id}.")
        else:
            conn.commit()
            print(f".Ponto > {id} < deleted.")

    except Exception as e:
        print(f"> An error occurred: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    cli(prog_name='main')