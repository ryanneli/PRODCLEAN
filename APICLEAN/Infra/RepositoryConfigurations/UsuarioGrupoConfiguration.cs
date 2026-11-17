using ApiClean.Dominio.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace ApiClean.Infra.RepositoryConfigurations;

public class UsuarioGrupoConfiguration : IEntityTypeConfiguration<UsuarioGrupo>
{
    public void Configure(EntityTypeBuilder<UsuarioGrupo> builder)
    {
        builder.ToTable("UsuariosGrupos");
        builder.HasKey(x => new { x.UsuarioId, x.GrupoUsuarioId });
        builder.HasOne(x => x.Usuario).WithMany(x => x.Grupos)
            .HasForeignKey(x => x.UsuarioId).OnDelete(DeleteBehavior.Cascade);
        builder.HasOne(x => x.Grupo).WithMany(x => x.Usuarios)
            .HasForeignKey(x => x.GrupoUsuarioId).OnDelete(DeleteBehavior.Cascade);
    }
}
