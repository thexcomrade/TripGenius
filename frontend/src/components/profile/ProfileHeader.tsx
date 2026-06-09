"use client";

interface UserProfile {
    uid: string;
    tripgenius_id: string;
    full_name: string;
    username: string;
    email: string;
    bio: string;
    country: string;
    profile_image: string;
    total_trips: number;
    saved_trips: number;
    eco_score: number;
    countries_visited: number;
    is_verified: boolean;
    created_at: string;
    travel_preferences: string[];
}

interface ProfileHeaderProps {
    user: UserProfile;
    onSettingsClick: () => void;
    onEditProfileClick: () => void;
    onPhotoClick: () => void;
}

export default function ProfileHeader({
    user,
    onSettingsClick,
    onEditProfileClick,
    onPhotoClick
}: ProfileHeaderProps) {
    return (
        <section
            style={{
                width: "100%",
                maxWidth: "1100px",
                margin: "0 auto 40px auto",
                padding: "40px 30px"
            }}
        >
            <div
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    alignItems: "center",
                    gap: "50px"
                }}
            >
                {/* PROFILE IMAGE */}

                <div
                    style={{
                        position: "relative"
                    }}
                >
                    <div
                        style={{
                            width: "170px",
                            height: "170px",
                            borderRadius: "50%",
                            overflow: "hidden",
                            border:
                                "4px solid rgba(14,165,233,0.35)",
                            background:
                                "linear-gradient(135deg,#0EA5E9,#14B8A6)",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            boxShadow:
                                "0 0 30px rgba(14,165,233,0.25)"
                        }}
                    >
                        {user.profile_image ? (
                            <img
                                src={
                                    user.profile_image
                                }
                                alt="Profile"
                                style={{
                                    width: "100%",
                                    height: "100%",
                                    objectFit:
                                        "cover"
                                }}
                            />
                        ) : (
                            <span
                                style={{
                                    fontSize:
                                        "4rem",
                                    color:
                                        "#ffffff",
                                    fontWeight:
                                        800
                                }}
                            >
                                {user.full_name
                                    .charAt(0)
                                    .toUpperCase()}
                            </span>
                        )}
                    </div>

                    <button
                        onClick={
                            onPhotoClick
                        }
                        style={{
                            position:
                                "absolute",
                            right: 5,
                            bottom: 5,
                            width: "48px",
                            height: "48px",
                            borderRadius:
                                "50%",
                            border: "none",
                            cursor:
                                "pointer",
                            fontSize:
                                "1.2rem",
                            background:
                                "#0EA5E9",
                            color:
                                "#ffffff",
                            boxShadow:
                                "0 0 15px rgba(14,165,233,0.35)"
                        }}
                    >
                        📷
                    </button>
                </div>

                {/* PROFILE DETAILS */}

                <div
                    style={{
                        flex: 1,
                        minWidth: "300px"
                    }}
                >
                    {/* USERNAME ROW */}

                    <div
                        style={{
                            display:
                                "flex",
                            flexWrap:
                                "wrap",
                            alignItems:
                                "center",
                            gap: "14px",
                            marginBottom:
                                "20px"
                        }}
                    >
                        <h1
                            style={{
                                fontSize:
                                    "2rem",
                                fontWeight:
                                    700,
                                color:
                                    "#ffffff"
                            }}
                        >
                            @
                            {
                                user.username
                            }
                        </h1>

                        {user.is_verified && (
                            <span
                                style={{
                                    background:
                                        "#0EA5E9",
                                    color:
                                        "#ffffff",
                                    padding:
                                        "6px 12px",
                                    borderRadius:
                                        "999px",
                                    fontSize:
                                        "0.85rem",
                                    fontWeight:
                                        700
                                }}
                            >
                                ✓ Verified
                            </span>
                        )}

                        <button
                            onClick={
                                onEditProfileClick
                            }
                            style={{
                                padding:
                                    "10px 20px",
                                borderRadius:
                                    "12px",
                                border:
                                    "1px solid rgba(255,255,255,0.12)",
                                background:
                                    "rgba(255,255,255,0.08)",
                                color:
                                    "#ffffff",
                                cursor:
                                    "pointer",
                                fontWeight:
                                    600
                            }}
                        >
                            Edit Profile
                        </button>

                        <button
                            onClick={
                                onSettingsClick
                            }
                            style={{
                                width: "44px",
                                height: "44px",
                                borderRadius:
                                    "12px",
                                border:
                                    "1px solid rgba(255,255,255,0.12)",
                                background:
                                    "rgba(255,255,255,0.08)",
                                color:
                                    "#ffffff",
                                cursor:
                                    "pointer",
                                fontSize:
                                    "1.2rem"
                            }}
                        >
                            ⚙️
                        </button>
                    </div>

                    {/* STATS */}

                    <div
                        style={{
                            display:
                                "flex",
                            flexWrap:
                                "wrap",
                            gap: "35px",
                            marginBottom:
                                "25px"
                        }}
                    >
                        <div>
                            <strong>
                                {
                                    user.total_trips
                                }
                            </strong>{" "}
                            trips
                        </div>

                        <div>
                            <strong>
                                {
                                    user.saved_trips
                                }
                            </strong>{" "}
                            saved
                        </div>

                        <div>
                            <strong>
                                {
                                    user.eco_score
                                }
                            </strong>{" "}
                            eco score
                        </div>
                    </div>

                    {/* NAME */}

                    <h2
                        style={{
                            fontSize:
                                "1.3rem",
                            marginBottom:
                                "8px",
                            color:
                                "#ffffff"
                        }}
                    >
                        {
                            user.full_name
                        }
                    </h2>

                    {/* ID */}

                    <p
                        style={{
                            color:
                                "#38BDF8",
                            marginBottom:
                                "15px",
                            fontWeight:
                                600
                        }}
                    >
                        {
                            user.tripgenius_id
                        }
                    </p>

                    {/* BIO */}

                    <p
                        style={{
                            color:
                                "#CBD5E1",
                            lineHeight:
                                1.8,
                            maxWidth:
                                "650px"
                        }}
                    >
                        {user.bio}
                    </p>

                    {/* COUNTRY */}

                    <div
                        style={{
                            marginTop:
                                "18px"
                        }}
                    >
                        <span
                            style={{
                                display:
                                    "inline-block",
                                padding:
                                    "8px 16px",
                                borderRadius:
                                    "999px",
                                background:
                                    "rgba(14,165,233,0.15)",
                                color:
                                    "#7DD3FC",
                                fontWeight:
                                    600
                            }}
                        >
                            🌍 {user.country}
                        </span>
                    </div>
                </div>
            </div>
        </section>
    );
}