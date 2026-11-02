using UnrealBuildTool;
public class NUthEck : ModuleRules
{
    public NUthEck(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "Json" });
        PrivateDependencyModuleNames.AddRange(new string[] { "SlateCore", "MeshDescription", "StaticMeshDescription" });
    }
}
