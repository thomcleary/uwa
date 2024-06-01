// *** Task G
//
// Remove varying color variable and replace with vec4
// varying vec4 color;
//
// values from vertex shader
varying vec4 position;
varying vec3 normal;
varying vec2 texCoord;  // The third coordinate is always 0.0 and is discarded
//
// colour of fragment
vec4 color;
//
uniform vec3 AmbientProduct, DiffuseProduct, SpecularProduct;
uniform mat4 ModelView, Projection;
uniform float Shininess;
//
uniform vec4 LightPosition1;
//     *** Task H
uniform float LightBrightness1;
//     Task H ***
// Task G ***
//
// *** Task I
uniform vec4 LightPosition2;
uniform float LightBrightness2;
// Task I ***

uniform sampler2D texture;

//     *** Task B
uniform float texScale;
//     Task B *** 

void main()
{
    // *** Task G
    // Perform lighting calculations in the fragment shader

    // Transform vertex into eye coordinates
    vec3 pos = (ModelView * position).xyz;
    // The vector from the  first light to the fragment
    vec3 Lvec1 = LightPosition1.xyz - pos;

    // Unit direction vectors for Blinn-Phong shading calculation
    // Light1
    vec3 L1 = normalize(Lvec1);   // Direction to the light source
    vec3 E = normalize(-pos);   // Direction to the eye/camera
    vec3 H1 = normalize(L1 + E);  // Halfway vector

    //     *** Task I
    //     vector from the second directional light to the fragment
    vec3 Lvec2 = LightPosition2.xyz - pos;

    //     Unit direction vectors for Blinn-Phong shading calculation
    //     Light2
    vec3 L2 = normalize(Lvec2);   // Direction to the light source
    vec3 H2 = normalize(L2 + E);  // Halfway vector

    //     Transform vertex normal into eye coordinates (assumes scaling
    //     is uniform across dimensions)
    vec3 N = normalize((ModelView*vec4(normal, 0.0)).xyz);


    // G. Compute terms in the illumination equation
    vec3 ambient1   = AmbientProduct * LightBrightness1;
    vec3 ambient2   = AmbientProduct * LightBrightness2;

    float Kd1       = max( dot(L1, N), 0.0 );
    vec3  diffuse1  = Kd1 * DiffuseProduct * LightBrightness1;

    float Kd2       = max( dot(L2, N), 0.0 );
    vec3  diffuse2  = Kd2 * DiffuseProduct * LightBrightness2;

    float Ks1       = pow( max(dot(N, H1), 0.0), Shininess );
    //         *** Task H
    //         increase specular by brightness
    vec3  specular1 = Ks1 * SpecularProduct * LightBrightness1;
    //         Task H ***

    float Ks2       = pow( max(dot(N, H2), 0.0), Shininess );
    vec3  specular2 = Ks2 * SpecularProduct * LightBrightness2;
    

    if (dot(L1, N) < 0.0 ) {
	specular1 = vec3(0.0, 0.0, 0.0);
    } 
    if (dot(L2, N) < 0.0 ) {
	specular2 = vec3(0.0, 0.0, 0.0);
    } 

    // G. globalAmbient is independent of distance from the light source
    vec3 globalAmbient = vec3(0.1, 0.1, 0.1);

    //          *** Task F 
    //
    //         Define a scalar to reduce the rgb of the vertex dependant on
    //         the distance from the light source to the vertex
    //
    float NON_ZERO_VALUE = 0.01; // to avoid division by zero if the length of Lvec is 0
    float vertexToLightDist = length(Lvec1);

    //         As the vertex->lightSource distance decreases, the lightIntensity increases
    //         The inverse occurs for a distance increase, the intensity decreases
    float lightIntensity = 1.0 / (NON_ZERO_VALUE + vertexToLightDist);
    //         lightIntensity is a scalar that adjusts the sum of the
    //         ambient, diffuse and specular light for a sceneObj

    //             *** Task H 
    //             remove specular from color of fragment
    //
    //     I. Add directional light's ambient and diffuse
    //     (not affected by distance)
    color.rgb = globalAmbient  + 
                ((ambient1 + diffuse1) * lightIntensity) +
                ambient2 +
                diffuse2;
    //             Task H ***
    //         Task F ***
    //
    color.a = 1.0;
    //
    //         *** Task B
    //
    //         From "The Book of Shaders" by Patricio Gonzalez Vivo
    //         - coord (second argument to texture2D)specifies the texture 
    //           coordinates at which texture will be sampled.
    //
    //         Therefore we scale the texCoord vector by the sceneObjects
    //         texture scaling scaler value
    //
    //             *** Task H
    //             // add specular values to the fragment colour
    //
    //     I. Add directional light's specular value (not affected by distance)
    gl_FragColor = color * 
                   texture2D( texture, texCoord * texScale ) +
                   vec4(specular1 * lightIntensity + specular2, 1.0);
    //             Task H ***
    //         Task B ***
    //     Task I ***
    // Task G ***
}