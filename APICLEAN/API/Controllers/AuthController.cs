using ApiClean.Application.DTO;
using ApiClean.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace ApiClean.API.Controllers;

[ApiController]
[Route("api/auth")]
public sealed class AuthController(IAuthService authService) : ControllerBase
{
    [HttpPost("register")]
    [ProducesResponseType(typeof(AuthResponseDto), StatusCodes.Status201Created)]
    [ProducesResponseType(StatusCodes.Status400BadRequest)]
    [ProducesResponseType(StatusCodes.Status409Conflict)]
    public async Task<ActionResult<AuthResponseDto>> Register(
        RegisterDto dto,
        CancellationToken cancellationToken)
    {
        try
        {
            var resposta = await authService.RegistrarAsync(dto, cancellationToken);
            return StatusCode(StatusCodes.Status201Created, resposta);
        }
        catch (ArgumentException exception)
        {
            return BadRequest(new { message = exception.Message });
        }
        catch (InvalidOperationException exception)
        {
            return Conflict(new { message = exception.Message });
        }
    }

    [HttpPost("login")]
    [ProducesResponseType(typeof(AuthResponseDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status401Unauthorized)]
    public async Task<ActionResult<AuthResponseDto>> Login(
        LoginDto dto,
        CancellationToken cancellationToken)
    {
        var resposta = await authService.LoginAsync(dto, cancellationToken);
        return resposta is null
            ? Unauthorized(new { message = "Usuário ou senha inválidos." })
            : Ok(resposta);
    }
}
