// INGSRegistry.sol
// Versão: 1.0.5
// Responsabilidade: Registro de personas e interações no blockchain para o INGS Protocol
// Data: 2025-04-23
// Assinatura: Product Owner: Zeh Sobrinho; Scrum Team: GPT, Qwen, Gemini, Grok, DeepSeek

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract INGSRegistry {
    struct Persona {
        string personaId;
        address walletAddress;
        string modelType;
        uint256 createdAt;
    }

    struct Interaction {
        string personaId;
        string message;
        string response;
        string mode;
        uint256 timestamp;
    }

    mapping(string => Persona) public personas;
    mapping(uint256 => Interaction) public interactions;
    uint256 public interactionCount;

    event PersonaRegistered(string personaId, address walletAddress, string modelType);
    event InteractionLogged(string personaId, string message, string response, string mode);

    function registerPersona(string memory _personaId, address _walletAddress, string memory _modelType) public {
        personas[_personaId] = Persona(_personaId, _walletAddress, _modelType, block.timestamp);
        emit PersonaRegistered(_personaId, _walletAddress, _modelType);
    }

    function logInteraction(string memory _personaId, string memory _message, string memory _response, string memory _mode) public {
        interactions[interactionCount] = Interaction(_personaId, _message, _response, _mode, block.timestamp);
        interactionCount++;
        emit InteractionLogged(_personaId, _message, _response, _mode);
    }
}