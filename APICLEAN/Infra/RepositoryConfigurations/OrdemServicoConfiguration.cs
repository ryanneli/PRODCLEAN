using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class OrdemServicoConfiguration : IEntityTypeConfiguration<OrdemServico>
{
    public void Configure(EntityTypeBuilder<OrdemServico> builder)
    {
        builder.ToTable("producao_ordemservico");
        builder.HasKey(x => x.Rcp);
        builder.Property(x => x.Os).HasMaxLength(20).IsRequired();
        builder.Property(x => x.Cliente).HasMaxLength(100).IsRequired();
        builder.Property(x => x.Proposta).HasMaxLength(50);
        builder.Property(x => x.NfSaida).HasMaxLength(50);
        builder.Property(x => x.TipoServico).HasMaxLength(100);
        builder.Property(x => x.Prioridade).HasMaxLength(30).IsRequired();
        builder.Property(x => x.LiberadoPor).HasMaxLength(100);
        builder.Property(x => x.NfCliente).HasMaxLength(50);
        builder.Property(x => x.NomeMotorista).HasMaxLength(100);
        builder.Property(x => x.PlacaVeiculo).HasMaxLength(20);
        builder.Property(x => x.ExpedidoPor).HasMaxLength(50);
        builder.Property(x => x.Status).HasMaxLength(30).IsRequired();
        builder.Property(x => x.Operador).HasMaxLength(200);
        builder.HasIndex(x => x.Os);
        builder.HasIndex(x => x.Cliente);
    }
}
