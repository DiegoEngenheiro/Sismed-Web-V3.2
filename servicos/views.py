from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormServico
from django.http import HttpResponse, FileResponse
from .models import Servico, ServicoAdicional
from fpdf import FPDF
from io import BytesIO
from django.conf import settings
from django.contrib import messages
from urllib.parse import quote

def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'novo_servico.html', {'form': form})
    elif request.method == "POST":
        form = FormServico(request.POST)
        if form.is_valid():
            servico = form.save()  # Salva o serviço e obtém o objeto salvo

            # Busca o número de telefone do cliente
            numero_cliente = servico.cliente.celular  # Supondo que o campo do celular seja 'celular'

            # Obtém as categorias de consulta associadas ao serviço
            categorias = servico.categoria_Consulta.all()
            especialidades = ", ".join([categoria.get_titulo_display() for categoria in categorias])  # Usa get_titulo_display()

            # Formata a data no formato brasileiro (DD/MM/AAAA)
            data_formatada = servico.data_agendada.strftime("%d/%m/%Y")

            # Cria a mensagem para o WhatsApp
            mensagem = (
                f"Olá {servico.cliente.nome}, sua consulta foi agendada!\n"
                f"Especialidade: {especialidades}\n"  # Exibe os rótulos das especialidades
                f"Data: {data_formatada}\n"  # Data formatada no padrão brasileiro
                f"Horário: {servico.horario}\n"
                f"Local: {servico.local}\n"
                f"Agradecemos pela preferência!"
            )

            # Redireciona para o WhatsApp Web
            return abrir_whatsapp(request, numero_cliente, mensagem)
        else:
            # Se o formulário não for válido, exibe os erros
            return render(request, 'novo_servico.html', {'form': form})

def abrir_whatsapp(request, numero, mensagem):
    # Codifica a mensagem para uso na URL
    mensagem_codificada = quote(mensagem)
    
    # Cria a URL do WhatsApp Web
    url_whatsapp = f"https://web.whatsapp.com/send?phone={numero}&text={mensagem_codificada}"
    
    # Redireciona o usuário para o WhatsApp Web
    return redirect(url_whatsapp)

def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, 'listar_servico.html', {'servicos': servicos})
    
def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servico.html', {'servico': servico})

def gerar_os(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)

    pdf.set_fill_color(240,240,240)
    pdf.cell(35, 10, 'Cliente:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.cliente.nome}', 1, 1, 'L', 1)

    pdf.cell(35, 10, 'Consultas:', 1, 0, 'L', 1)

    categorias_Consulta = servico.categoria_Consulta.all()
    for i, Consulta in enumerate(categorias_Consulta):
        pdf.cell(0, 10, f'- {Consulta.get_titulo_display()}', 1, 1, 'L', 1)
        if not i == len(categorias_Consulta) -1:
            pdf.cell(35, 10, '', 0, 0)

    pdf.cell(35, 10, 'Data de início:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_inicio}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Data de entrega:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.data_entrega}', 1, 1, 'L', 1)
    pdf.cell(35, 10, 'Protocolo:', 1, 0, 'L', 1)
    pdf.cell(0, 10, f'{servico.protocole}', 1, 1, 'L', 1)
    
    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)
   
    return FileResponse(pdf_bytes, as_attachment=True, filename=f"os-{servico.protocole}.pdf")

def servico_adicional(request):
    identificador_servico = request.POST.get('identificador_servico')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    preco = request.POST.get('preco')

    servico_adicional = ServicoAdicional(titulo=titulo,
                                        descricao=descricao,
                                        preco=preco)
    
    servico_adicional.save()

    servico = Servico.objects.get(identificador=identificador_servico)
    servico.servicos_adicionais.add(servico_adicional)
    servico.save()

    return HttpResponse("Salvo")

def excluir_servico(request, identificador):
    # Busca o serviço pelo identificador
    servico = get_object_or_404(Servico, identificador=identificador)
    
    # Exclui o serviço
    servico.delete()
    
    # Mensagem de sucesso
    messages.success(request, 'Serviço excluído com sucesso!')
    
    # Redireciona para a lista de serviços
    return redirect('listar_servico')