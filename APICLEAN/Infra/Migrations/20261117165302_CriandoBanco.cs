using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace ApiClean.Infra.Migrations
{
    /// <inheritdoc />
    public partial class CriandoBanco : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "GruposUsuarios",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Nome = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_GruposUsuarios", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "producao_funcionarioproducao",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Nome = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Ativo = table.Column<bool>(type: "bit", nullable: false),
                    CriadoEm = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_funcionarioproducao", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "producao_grupochat",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Nome = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: true),
                    CriadoEm = table.Column<DateTime>(type: "datetime2", nullable: false),
                    EGrupo = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_grupochat", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "producao_notificacaosetor",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    SetorDestino = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    Mensagem = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    DataCriacao = table.Column<DateTime>(type: "datetime2", nullable: false),
                    RcpNumero = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_notificacaosetor", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "producao_ordemservico",
                columns: table => new
                {
                    Rcp = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    EditandoPorId = table.Column<int>(type: "int", nullable: true),
                    EditandoDesde = table.Column<DateTime>(type: "datetime2", nullable: true),
                    Version = table.Column<int>(type: "int", nullable: false),
                    Os = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    Cliente = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Proposta = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    NfSaida = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    TipoServico = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    Prioridade = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                    DataLiberacao = table.Column<DateTime>(type: "datetime2", nullable: true),
                    LiberadoPor = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    ObservacaoComercial = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    NfCliente = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    DataEntradaPeca = table.Column<DateTime>(type: "datetime2", nullable: true),
                    DescricaoPeca = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    ObsQualidade = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    PrevisaoEntregaQualidade = table.Column<DateTime>(type: "datetime2", nullable: true),
                    DataInspecaoInicial = table.Column<DateTime>(type: "datetime2", nullable: true),
                    NomeMotorista = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    PlacaVeiculo = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: true),
                    ObsExpedicao = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    DataExpedicao = table.Column<DateTime>(type: "datetime2", nullable: true),
                    ExpedidoPor = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    Status = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                    InicioProducao = table.Column<DateTime>(type: "datetime2", nullable: true),
                    Operador = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    PrevisaoConclusaoProd = table.Column<DateTime>(type: "datetime2", nullable: true),
                    DataFinalizaProducao = table.Column<DateTime>(type: "datetime2", nullable: true),
                    ObsProducao = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    DataInspecaoFinal = table.Column<DateTime>(type: "datetime2", nullable: true),
                    CertificadoPdf = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_ordemservico", x => x.Rcp);
                });

            migrationBuilder.CreateTable(
                name: "Usuarios",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    NomeUsuario = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: false),
                    Email = table.Column<string>(type: "nvarchar(254)", maxLength: 254, nullable: false),
                    SenhaHash = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    Ativo = table.Column<bool>(type: "bit", nullable: false),
                    CriadoEm = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Usuarios", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "producao_grupochat_membros",
                columns: table => new
                {
                    GrupoChatId = table.Column<int>(type: "int", nullable: false),
                    UsuarioId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_grupochat_membros", x => new { x.GrupoChatId, x.UsuarioId });
                    table.ForeignKey(
                        name: "FK_producao_grupochat_membros_producao_grupochat_GrupoChatId",
                        column: x => x.GrupoChatId,
                        principalTable: "producao_grupochat",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_mensagem",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    GrupoId = table.Column<int>(type: "int", nullable: false),
                    AutorId = table.Column<int>(type: "int", nullable: false),
                    Texto = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    DataEnvio = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Editada = table.Column<bool>(type: "bit", nullable: false),
                    DataEdicao = table.Column<DateTime>(type: "datetime2", nullable: true),
                    Lida = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_mensagem", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_mensagem_producao_grupochat_GrupoId",
                        column: x => x.GrupoId,
                        principalTable: "producao_grupochat",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_notificacaosetor_usuarios_que_leram",
                columns: table => new
                {
                    NotificacaoSetorId = table.Column<int>(type: "int", nullable: false),
                    UsuarioId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_notificacaosetor_usuarios_que_leram", x => new { x.NotificacaoSetorId, x.UsuarioId });
                    table.ForeignKey(
                        name: "FK_producao_notificacaosetor_usuarios_que_leram_producao_notificacaosetor_NotificacaoSetorId",
                        column: x => x.NotificacaoSetorId,
                        principalTable: "producao_notificacaosetor",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_certificadorcp",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RcpId = table.Column<int>(type: "int", nullable: false),
                    Arquivo = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    NomeExibicao = table.Column<string>(type: "nvarchar(255)", maxLength: 255, nullable: false),
                    DataUpload = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_certificadorcp", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_certificadorcp_producao_ordemservico_RcpId",
                        column: x => x.RcpId,
                        principalTable: "producao_ordemservico",
                        principalColumn: "Rcp",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_rcpfoto",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RcpId = table.Column<int>(type: "int", nullable: false),
                    Imagem = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    DataUpload = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Tipo = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_rcpfoto", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_rcpfoto_producao_ordemservico_RcpId",
                        column: x => x.RcpId,
                        principalTable: "producao_ordemservico",
                        principalColumn: "Rcp",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_registropecamatada",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    FuncionarioId = table.Column<int>(type: "int", nullable: false),
                    Quantidade = table.Column<int>(type: "int", nullable: false),
                    DataOcorrencia = table.Column<DateTime>(type: "datetime2", nullable: false),
                    Motivo = table.Column<string>(type: "nvarchar(255)", maxLength: 255, nullable: true),
                    Resolucao = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    OsRelacionadaId = table.Column<int>(type: "int", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_registropecamatada", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_registropecamatada_producao_funcionarioproducao_FuncionarioId",
                        column: x => x.FuncionarioId,
                        principalTable: "producao_funcionarioproducao",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_producao_registropecamatada_producao_ordemservico_OsRelacionadaId",
                        column: x => x.OsRelacionadaId,
                        principalTable: "producao_ordemservico",
                        principalColumn: "Rcp",
                        onDelete: ReferentialAction.SetNull);
                });

            migrationBuilder.CreateTable(
                name: "UsuariosGrupos",
                columns: table => new
                {
                    UsuarioId = table.Column<int>(type: "int", nullable: false),
                    GrupoUsuarioId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_UsuariosGrupos", x => new { x.UsuarioId, x.GrupoUsuarioId });
                    table.ForeignKey(
                        name: "FK_UsuariosGrupos_GruposUsuarios_GrupoUsuarioId",
                        column: x => x.GrupoUsuarioId,
                        principalTable: "GruposUsuarios",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_UsuariosGrupos_Usuarios_UsuarioId",
                        column: x => x.UsuarioId,
                        principalTable: "Usuarios",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_logedicaomensagem",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    MensagemId = table.Column<int>(type: "int", nullable: false),
                    TextoAntigo = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    DataAlteracao = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_logedicaomensagem", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_logedicaomensagem_producao_mensagem_MensagemId",
                        column: x => x.MensagemId,
                        principalTable: "producao_mensagem",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "producao_fotopecamatada",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    RegistroId = table.Column<int>(type: "int", nullable: false),
                    Tipo = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    Imagem = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    DataUpload = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_producao_fotopecamatada", x => x.Id);
                    table.ForeignKey(
                        name: "FK_producao_fotopecamatada_producao_registropecamatada_RegistroId",
                        column: x => x.RegistroId,
                        principalTable: "producao_registropecamatada",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_GruposUsuarios_Nome",
                table: "GruposUsuarios",
                column: "Nome",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_producao_certificadorcp_RcpId",
                table: "producao_certificadorcp",
                column: "RcpId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_fotopecamatada_RegistroId",
                table: "producao_fotopecamatada",
                column: "RegistroId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_funcionarioproducao_Nome",
                table: "producao_funcionarioproducao",
                column: "Nome",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_producao_grupochat_EGrupo",
                table: "producao_grupochat",
                column: "EGrupo");

            migrationBuilder.CreateIndex(
                name: "IX_producao_grupochat_membros_UsuarioId",
                table: "producao_grupochat_membros",
                column: "UsuarioId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_logedicaomensagem_MensagemId",
                table: "producao_logedicaomensagem",
                column: "MensagemId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_mensagem_AutorId",
                table: "producao_mensagem",
                column: "AutorId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_mensagem_GrupoId",
                table: "producao_mensagem",
                column: "GrupoId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_notificacaosetor_DataCriacao",
                table: "producao_notificacaosetor",
                column: "DataCriacao");

            migrationBuilder.CreateIndex(
                name: "IX_producao_notificacaosetor_RcpNumero",
                table: "producao_notificacaosetor",
                column: "RcpNumero");

            migrationBuilder.CreateIndex(
                name: "IX_producao_notificacaosetor_usuarios_que_leram_UsuarioId",
                table: "producao_notificacaosetor_usuarios_que_leram",
                column: "UsuarioId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_ordemservico_Cliente",
                table: "producao_ordemservico",
                column: "Cliente");

            migrationBuilder.CreateIndex(
                name: "IX_producao_ordemservico_Os",
                table: "producao_ordemservico",
                column: "Os");

            migrationBuilder.CreateIndex(
                name: "IX_producao_rcpfoto_RcpId",
                table: "producao_rcpfoto",
                column: "RcpId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_registropecamatada_FuncionarioId",
                table: "producao_registropecamatada",
                column: "FuncionarioId");

            migrationBuilder.CreateIndex(
                name: "IX_producao_registropecamatada_OsRelacionadaId",
                table: "producao_registropecamatada",
                column: "OsRelacionadaId");

            migrationBuilder.CreateIndex(
                name: "IX_Usuarios_Email",
                table: "Usuarios",
                column: "Email",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Usuarios_NomeUsuario",
                table: "Usuarios",
                column: "NomeUsuario",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_UsuariosGrupos_GrupoUsuarioId",
                table: "UsuariosGrupos",
                column: "GrupoUsuarioId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "producao_certificadorcp");

            migrationBuilder.DropTable(
                name: "producao_fotopecamatada");

            migrationBuilder.DropTable(
                name: "producao_grupochat_membros");

            migrationBuilder.DropTable(
                name: "producao_logedicaomensagem");

            migrationBuilder.DropTable(
                name: "producao_notificacaosetor_usuarios_que_leram");

            migrationBuilder.DropTable(
                name: "producao_rcpfoto");

            migrationBuilder.DropTable(
                name: "UsuariosGrupos");

            migrationBuilder.DropTable(
                name: "producao_registropecamatada");

            migrationBuilder.DropTable(
                name: "producao_mensagem");

            migrationBuilder.DropTable(
                name: "producao_notificacaosetor");

            migrationBuilder.DropTable(
                name: "GruposUsuarios");

            migrationBuilder.DropTable(
                name: "Usuarios");

            migrationBuilder.DropTable(
                name: "producao_funcionarioproducao");

            migrationBuilder.DropTable(
                name: "producao_ordemservico");

            migrationBuilder.DropTable(
                name: "producao_grupochat");
        }
    }
}
