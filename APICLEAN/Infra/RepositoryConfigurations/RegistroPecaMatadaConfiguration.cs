using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class RegistroPecaMatadaConfiguration : IEntityTypeConfiguration<RegistroPecaMatada>
{
    public void Configure(EntityTypeBuilder<RegistroPecaMatada> builder)
    {
        builder.ToTable("producao_registropecamatada");
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Motivo).HasMaxLength(255);
        builder.HasIndex(x => x.FuncionarioId);
        builder.HasIndex(x => x.OsRelacionadaId);
        builder.HasOne(x => x.Funcionario).WithMany(x => x.Perdas).HasForeignKey(x => x.FuncionarioId).OnDelete(DeleteBehavior.Cascade);
        builder.HasOne(x => x.OsRelacionada).WithMany(x => x.PerdasPecas).HasForeignKey(x => x.OsRelacionadaId).OnDelete(DeleteBehavior.SetNull);
    }
}
