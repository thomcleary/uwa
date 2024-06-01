attribute vec3 vPosition;
attribute vec3 vNormal;
attribute vec2 vTexCoord;

// *** Task G
//
// Remove varying color variable
// varying vec4 color;
varying vec4 position;
varying vec3 normal;
//
// Task G ***
varying vec2 texCoord;

uniform mat4 ModelView;
uniform mat4 Projection;

void main()
{
    // *** Task G
    //
    position = vec4(vPosition, 1.0);
    normal = vNormal;
    texCoord = vTexCoord;

    gl_Position = Projection * ModelView * position;
    // Task G ***


    // THIS TASK HAS BEEN COMMENTED OUT TO SHOW THE WORKING FOR TASK F
    // HOWEVER THE VARIABLES TO MAKE IT WORK NO LONGER EXIST IN THIS FILE
    // AS THE LIGHTING IS NOW PERFORMED IN fStart.glsl
    //
    // // *** Task F 
    // //
    // // Define a scalar to reduce the rgb of the vertex dependant on
    // // the distance from the light source to the vertex
    // //
    // float NON_ZERO_VALUE = 0.01; // to avoid division by zero if the length of Lvec is 0
    // float vertexToLightDist = length(Lvec);

    // // As the vertex->lightSource distance decreases, the lightIntensity increases
    // // The inverse occurs for a distance increase, the intensity decreases
    // float lightIntensity = 1.0 / (NON_ZERO_VALUE + vertexToLightDist);

    // // lightIntensity is a scalar that adjusts the sum of the
    // // ambient, diffuse and specular light for a sceneObj
    // color.rgb = globalAmbient  + ( (ambient + diffuse + specular) * lightIntensity );
    // //
    // //  Task F ***
}